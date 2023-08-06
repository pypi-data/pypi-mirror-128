from __future__ import annotations
import chily
import hmac
import json
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from typing import Any, List, Tuple, TYPE_CHECKING, Iterator
from dataclasses import dataclass

from .api import Endpoints
from .authentication import Auth, Sigma
from .proto.data_room_pb2 import DataRoom
from .proto.attestation_pb2 import AttestationSpecification, Fatquote
from .proto.delta_enclave_api_pb2 import (DataNoncePubkey, Request, Response)
from .proto.gcg_pb2 import (
    CreateDataRoomRequest, CreateDataRoomResponse,
    ExecuteComputeRequest, ExecuteComputeResponse, GcgRequest, GcgResponse, GetResultsRequest,
    GetResultsResponseChunk, GetResultsResponseFooter, JobStatusRequest, JobStatusResponse,
    PublishDatasetToDataRoomRequest, PublishDatasetToDataRoomResponse,
    RemovePublishedDatasetRequest, RemovePublishedDatasetResponse,
    RetrieveAuditLogRequest, RetrieveAuditLogResponse, RetrieveDataRoomRequest,
    RetrieveDataRoomResponse, RetrieveDataRoomStatusRequest,
    RetrieveDataRoomStatusResponse, RetrievePublishedDatasetsRequest,
    RetrievePublishedDatasetsResponse, UpdateDataRoomStatusRequest,
    UpdateDataRoomStatusResponse, DataRoomStatus
)
from .proto.length_delimited import parse_length_delimited, serialize_length_delimited
from .storage import Key
from .types import FatquoteResBody, EnclaveMessage, ScopeTypes
from .verification import QuoteBody, Verification

if TYPE_CHECKING:
    from .client import Client

__all__ = ["Session", "VerificationOptions"]


def datanoncepubkey_to_message(
        encrypted_data: bytes,
        nonce: bytes,
        pubkey: bytes,
        sigma_auth: Sigma
) -> bytes:
    message = DataNoncePubkey()
    message.data = encrypted_data
    message.nonce = nonce
    message.pubkey = pubkey
    message.pki.certChainPem = sigma_auth.get_cert_chain()
    message.pki.signature = sigma_auth.get_signature()
    message.pki.idMac = sigma_auth.get_mac_tag()
    return serialize_length_delimited(message)


def message_to_datanoncepubkey(message: bytes) -> Tuple[bytes, bytes, bytes]:
    parsed_msg = DataNoncePubkey()
    parse_length_delimited(message, parsed_msg)
    return (parsed_msg.data, parsed_msg.nonce, parsed_msg.pubkey)


@dataclass
class VerificationOptions():
    """ Customize verification options """
    accept_debug: bool
    """ Accept enclaves with `DEBUG` flag """
    accept_configuration_needed: bool
    """ Accept enclaves with `CONFIGURATION_NEEDED` flag """
    accept_group_out_of_date: bool
    """ Accept enclaves with `GROUP_OUT_OF_DATE` flag """


class Session():
    """
    This class manages the communication with an enclave
    """
    client: Client
    session_id: str
    enclave_identifier: str
    auth: Auth
    email: str
    keypair: Any
    fatquote: Fatquote
    quote: QuoteBody

    def __init__(
            self,
            client: Client,
            session_id: str,
            driver_attestation_specification: AttestationSpecification,
            auth: Auth,
            email: str,
    ):
        """
        Create a new `Session` instance using `decentriq_platform.Client.create_session`
        """
        url = Endpoints.SESSION_FATQUOTE.replace(":sessionId", session_id)
        response: FatquoteResBody = client.api.get(url).json()
        fatquote_bytes = b64decode(response["fatquoteBase64"])
        fatquote = Fatquote()
        fatquote.ParseFromString(fatquote_bytes)
        verification = Verification(attestation_specification=driver_attestation_specification)
        report_data = verification.verify(fatquote)
        self.client = client
        self.session_id = session_id
        self.auth = auth
        self.email = email
        self.keypair = chily.Keypair.from_random()
        self.fatquote = fatquote
        self.report_data = report_data

    def _get_enclave_pubkey(self):
        pub_keyB = bytearray(self.report_data[:32])
        return chily.PublicKey.from_bytes(pub_keyB)

    def _encrypt_and_encode_data(self, data: bytes, auth: Auth) -> bytes:
        nonce = chily.Nonce.from_random()
        cipher = chily.Cipher(
            self.keypair.secret, self._get_enclave_pubkey()
        )
        enc_data = cipher.encrypt(data, nonce)
        public_keys = bytes(self.keypair.public_key.bytes) + bytes(self._get_enclave_pubkey().bytes)
        signature = auth._sign(public_keys)
        shared_key = bytes(self.keypair.secret.diffie_hellman(self._get_enclave_pubkey()).bytes)
        hkdf = HKDF(algorithm=hashes.SHA512(), length=64, info=b"IdP KDF Context", salt=b"")
        mac_key = hkdf.derive(shared_key)
        mac_tag = hmac.digest(mac_key, auth._get_user_id().encode(), "sha512")
        sigma_auth = Sigma(signature, mac_tag, auth)
        return datanoncepubkey_to_message(
            bytes(enc_data),
            bytes(nonce.bytes),
            bytes(self.keypair.public_key.bytes),
            sigma_auth
        )

    def _decode_and_decrypt_data(self, data: bytes) -> bytes:
        dec_data, nonceB, _ = message_to_datanoncepubkey(data)
        cipher = chily.Cipher(
            self.keypair.secret, self._get_enclave_pubkey()
        )
        return cipher.decrypt(dec_data, chily.Nonce.from_bytes(nonceB))

    def send_request(
            self,
            request: GcgRequest,
    ) -> List[GcgResponse]:
        serialized_request = serialize_length_delimited(
            Request(
                deltaRequest=self._encrypt_and_encode_data(
                    serialize_length_delimited(request),
                    self.auth
                )
            )
        )
        url = Endpoints.SESSION_MESSAGES.replace(":sessionId", self.session_id)
        enclave_request = EnclaveMessage(data=b64encode(serialized_request).decode("ascii"))
        enclave_response: EnclaveMessage = self.client.api.post(
            url, json.dumps(enclave_request), {"Content-type": "application/json"}
        ).json()
        enclave_response_bytes = b64decode(enclave_response["data"])

        responses: List[GcgResponse] = []
        offset = 0
        while offset < len(enclave_response_bytes):
            response_container = Response()
            offset += parse_length_delimited(enclave_response_bytes[offset:], response_container)
            if response_container.HasField("unsuccessfulResponse"):
                raise Exception(response_container.unsuccessfulResponse)
            else:
                response = GcgResponse()
                decrypted_response = self._decode_and_decrypt_data(
                    response_container.successfulResponse
                )
                parse_length_delimited(decrypted_response, response)
                if response.HasField("failure"):
                    raise Exception(response.failure)
                responses.append(response)
        return responses

    def create_data_room(
            self,
            data_room_definition: DataRoom
    ) -> CreateDataRoomResponse:
        """
        Create a DataRoom with the provided protobuf `data_room` configuration object
        """
        scope_id = self.client._ensure_scope_with_metadata(self.email, {"type": ScopeTypes.DATA_ROOM_DEFINITION})
        request = CreateDataRoomRequest(
            dataRoom=data_room_definition,
            scope=bytes.fromhex(scope_id)
        )
        responses = self.send_request(GcgRequest(createDataRoomRequest=request))
        if len(responses) != 1:
            raise Exception("Malformed response")
        response = responses[0]
        if not response.HasField("createDataRoomResponse"):
            raise Exception(
                "Expected createDataRoomResponse, got "
                + str(response.WhichOneof("gcg_response"))
            )
        return response.createDataRoomResponse

    def update_data_room_status(
            self,
            data_room_id: bytes,
            status: DataRoomStatus.V
    ) -> UpdateDataRoomStatusResponse:
        """
        Updates the status of the DataRoom
        """
        scope_id = self.client._ensure_scope_with_metadata(
            self.email,
            {
                "type": ScopeTypes.DATA_ROOM_INTERMEDIATE_DATA,
                "data_room_id": data_room_id.hex()
            }
        )
        request = UpdateDataRoomStatusRequest(
            dataRoomId=data_room_id,
            status=status,
            scope=bytes.fromhex(scope_id)
        )
        responses = self.send_request(GcgRequest(updateDataRoomStatusRequest=request))
        if len(responses) != 1:
            raise Exception("Malformed response")
        response = responses[0]
        if not response.HasField("updateDataRoomStatusResponse"):
            raise Exception(
                "Expected updateDataRoomStatusResponse, got "
                + str(response.WhichOneof("gcg_response"))
            )
        return response.updateDataRoomStatusResponse

    def retrieve_data_room_status(
            self,
            data_room_id: bytes
    ) -> RetrieveDataRoomStatusResponse:
        """
        Returns the status of the DataRoom
        """
        scope_id = self.client._ensure_scope_with_metadata(
            self.email,
            {
                "type": ScopeTypes.DATA_ROOM_INTERMEDIATE_DATA,
                "data_room_id": data_room_id.hex()
            }
        )
        request = RetrieveDataRoomStatusRequest(
            dataRoomId=data_room_id,
            scope=bytes.fromhex(scope_id)
        )
        responses = self.send_request(GcgRequest(retrieveDataRoomStatusRequest=request))
        if len(responses) != 1:
            raise Exception("Malformed response")
        response = responses[0]
        if not response.HasField("retrieveDataRoomStatusResponse"):
            raise Exception(
                "Expected retrieveDataRoomStatusResponse, got "
                + str(response.WhichOneof("gcg_response"))
            )
        return response.retrieveDataRoomStatusResponse

    def retrieve_data_room_definition(
            self,
            data_room_id: bytes
    ) -> RetrieveDataRoomResponse:
        """
        Returns the underlying protobuf configuration object for the DataRoom
        """
        scope_id = self.client._ensure_scope_with_metadata(
            self.email,
            {
                "type": ScopeTypes.DATA_ROOM_INTERMEDIATE_DATA,
                "data_room_id": data_room_id.hex()
            }
        )
        request = RetrieveDataRoomRequest(
            dataRoomId=data_room_id,
            scope=bytes.fromhex(scope_id)
        )
        responses = self.send_request(GcgRequest(retrieveDataRoomRequest=request))
        if len(responses) != 1:
            raise Exception("Malformed response")
        response = responses[0]
        if not response.HasField("retrieveDataRoomResponse"):
            raise Exception(
                "Expected retrieveDataRoomResponse, got "
                + str(response.WhichOneof("gcg_response"))
            )
        return response.retrieveDataRoomResponse

    def retrieve_audit_log(
            self,
            data_room_id: bytes
    ) -> RetrieveAuditLogResponse:
        """
        Returns the audit log for the DataRoom
        """
        scope_id = self.client._ensure_scope_with_metadata(
            self.email,
            {
                "type": ScopeTypes.DATA_ROOM_INTERMEDIATE_DATA,
                "data_room_id": data_room_id.hex()
            }
        )
        request = RetrieveAuditLogRequest(
            dataRoomId=data_room_id,
            scope=bytes.fromhex(scope_id)
        )
        responses = self.send_request(GcgRequest(retrieveAuditLogRequest=request))
        if len(responses) != 1:
            raise Exception("Malformed response")
        response = responses[0]
        if not response.HasField("retrieveAuditLogResponse"):
            raise Exception(
                "Expected retrieveAuditLogResponse, got "
                + str(response.WhichOneof("gcg_response"))
            )
        return response.retrieveAuditLogResponse

    def publish_file(
            self,
            data_room_id: bytes,
            manifest_hash: bytes,
            leaf_name: str,
            encryption_key: Key,
    ) -> PublishDatasetToDataRoomResponse:
        """
        Publishes a file to the DataRoom
        """
        scope_id = self.client._ensure_scope_with_metadata(
            self.email,
            {
                "type": ScopeTypes.DATA_ROOM_INTERMEDIATE_DATA,
                "data_room_id": data_room_id.hex()
            }
        )
        request = PublishDatasetToDataRoomRequest(
            dataRoomId=data_room_id,
            datasetHash=manifest_hash,
            leafName=leaf_name,
            encryptionKey=encryption_key.material,
            scope=bytes.fromhex(scope_id)
        )
        responses = self.send_request(GcgRequest(publishDatasetToDataRoomRequest=request))
        if len(responses) != 1:
            raise Exception("Malformed response")
        response = responses[0]
        if not response.HasField("publishDatasetToDataRoomResponse"):
            raise Exception(
                "Expected publishDatasetToDataRoomResponse, got "
                + str(response.WhichOneof("gcg_response"))
            )
        return response.publishDatasetToDataRoomResponse

    def remove_published_file(
            self,
            data_room_id: bytes,
            manifest_hash: bytes,
            leaf_name: str,
    ) -> RemovePublishedDatasetResponse:
        """
        Removes a published file from the DataRoom
        """
        scope_id = self.client._ensure_scope_with_metadata(
            self.email,
            {
                "type": ScopeTypes.DATA_ROOM_INTERMEDIATE_DATA,
                "data_room_id": data_room_id.hex()
            }
        )
        request = RemovePublishedDatasetRequest(
            dataRoomId=data_room_id,
            datasetHash=manifest_hash,
            leafName=leaf_name,
            scope=bytes.fromhex(scope_id)
        )
        responses = self.send_request(GcgRequest(removePublishedDatasetRequest=request))
        if len(responses) != 1:
            raise Exception("Malformed response")
        response = responses[0]
        if not response.HasField("removePublishedDatasetResponse"):
            raise Exception(
                "Expected removePublishedDatasetResponse, got "
                + str(response.WhichOneof("gcg_response"))
            )
        return response.removePublishedDatasetResponse

    def retrieve_published_files(
            self,
            data_room_id: bytes,
    ) -> RetrievePublishedDatasetsResponse:
        """
        Returns the files published to the DataRoom
        """
        scope_id = self.client._ensure_scope_with_metadata(
            self.email,
            {
                "type": ScopeTypes.DATA_ROOM_INTERMEDIATE_DATA,
                "data_room_id": data_room_id.hex()
            }
        )
        request = RetrievePublishedDatasetsRequest(
            dataRoomId=data_room_id,
            scope=bytes.fromhex(scope_id)
        )
        responses = self.send_request(GcgRequest(retrievePublishedDatasetsRequest=request))
        if len(responses) != 1:
            raise Exception("Malformed response")
        response = responses[0]
        if not response.HasField("retrievePublishedDatasetsResponse"):
            raise Exception(
                "Expected retrievePublishedDatasetResponse, got "
                + str(response.WhichOneof("gcg_response"))
            )
        return response.retrievePublishedDatasetsResponse

    def submit_compute(
            self,
            data_room_id: bytes,
            goal_nodes: List[str],
    ) -> ExecuteComputeResponse:
        """
        Submits a computation request which will generate an execution plan to
        perform the computation of the goal nodes
        """
        scope_id = self.client._ensure_scope_with_metadata(
            self.email,
            {
                "type": ScopeTypes.DATA_ROOM_INTERMEDIATE_DATA,
                "data_room_id": data_room_id.hex()
            }
        )
        request = ExecuteComputeRequest(
            dataRoomId=data_room_id,
            computeNodeNames=goal_nodes,
            isDryRun=False,
            scope=bytes.fromhex(scope_id)
        )
        responses = self.send_request(GcgRequest(executeComputeRequest=request))
        if len(responses) != 1:
            raise Exception("Malformed response")
        response = responses[0]
        if not response.HasField("executeComputeResponse"):
            raise Exception(
                "Expected executeComputeResponse, got "
                + str(response.WhichOneof("gcg_response"))
            )
        return response.executeComputeResponse

    def get_job_status(
            self,
            job_id: bytes,
    ) -> JobStatusResponse:
        """
        Returns the status of the provided `job_id`
        """
        request = JobStatusRequest(
            jobId=job_id,
        )
        responses = self.send_request(GcgRequest(jobStatusRequest=request))
        if len(responses) != 1:
            raise Exception("Malformed response")
        response = responses[0]
        if not response.HasField("jobStatusResponse"):
            raise Exception(
                "Expected jobStatusResponse, got "
                + str(response.WhichOneof("gcg_response"))
            )
        return response.jobStatusResponse

    def stream_job_results(
            self,
            job_id: bytes,
            compute_node_name: str,
    ) -> Iterator[GetResultsResponseChunk]:
        """
        Streams the results of the provided `job_id`
        """
        request = GetResultsRequest(
            jobId=job_id,
            computeNodeName=compute_node_name,
        )
        responses = self.send_request(GcgRequest(getResultsRequest=request))
        for response in responses:
            if response.HasField("getResultsResponseChunk"):
                yield response.getResultsResponseChunk
            elif response.HasField("getResultsResponseFooter"):
                return
            else:
                raise Exception(
                    "Expected getResultsResponseChunk or getResultsResponseFooter, got "
                    + str(response.WhichOneof("gcg_response"))
                )
        raise Exception("Enclave connection aborted while streaming results")

    def get_job_results(
            self,
            job_id: bytes,
            compute_node_name: str,
    ) -> bytes:
        """
        Returns the results of the provided `job_id`
        """
        return b"".join(list(map(lambda chunk: chunk.data, self.stream_job_results(job_id, compute_node_name))))
