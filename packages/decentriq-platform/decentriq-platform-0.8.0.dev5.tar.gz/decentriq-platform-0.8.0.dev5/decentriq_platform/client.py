import hashlib
import json
import os
from threading import BoundedSemaphore
from concurrent import futures
from base64 import b64encode 
from typing import BinaryIO, List, Dict, Optional
from .api import API, Endpoints
from .authentication import generate_csr, generate_key, Auth
from .config import (
        DECENTRIQ_CLIENT_ID, DECENTRIQ_HOST, DECENTRIQ_PORT, DECENTRIQ_USE_TLS
)
from .session import Session
from .storage import Key, CsvChunker, create_encrypted_chunk, StorageCipher
from .types import (
    AttestationSpecsResponse, FileDescription, FinalizeUpload,
    UserCsrRequest, UserCsrResponse, CreateSessionRequest, SessionJsonResponse,
    AttestationSpec, UploadDescription, ChunkWrapper,
    CreateScopeRequest, ScopeJson, ScopeTypes
)
from .proto.attestation_pb2 import AttestationSpecification
import base64



class Client:
    """
    Implementation of the decentriq platform REST API

    This class provides a Python interface to all functionality provided by
    the decentriq platform <https://platform.decentriq.com>
    """

    def __init__(
            self,
            api_token: str,
            client_id: str = DECENTRIQ_CLIENT_ID,
            host: str = DECENTRIQ_HOST,
            port: int = DECENTRIQ_PORT,
            use_tls: bool = DECENTRIQ_USE_TLS,
    ):
        """
        Create a new client instance. The API token can be obtained in the user
        panel of the decentriq platform <https://platform.decentriq.com/tokens>
        """
        self.api = API(
            api_token,
            client_id,
            host,
            port,
            use_tls
        )

    def get_ca_root_certificate(self) -> bytes:
        """
        Returns the decentriq root certificate used by the decentriq identity provider
        """
        url = Endpoints.SYSTEM_CERTIFICATE_AUTHORITY
        response = self.api.get(url).json()
        return response["rootCertificate"].encode("utf-8")

    def get_attestation_specs(self) -> List[AttestationSpec]:
        """
        Returns the list of the currently deployed enclave services for which
        we can create a `decentriq_platform.session.Session` using `create_session`
        """
        url = Endpoints.SYSTEM_ATTESTATION_SPECS
        response: AttestationSpecsResponse = self.api.get(url).json()
        attestation_specs = []

        for spec_json in response["attestationSpecs"]:
            attestation_specification = AttestationSpecification()
            attestation_specification.ParseFromString(base64.b64decode(spec_json["spec"]))
            attestation_spec = AttestationSpec(name=spec_json["name"], version=spec_json["version"], proto=attestation_specification)
            attestation_specs.append(attestation_spec)

        return attestation_specs

    def create_auth(self, email: str) -> Auth:
        """
        Creates a `decentriq_platform.authentication.Auth` object which can be
        attached to a `decentriq_platform.session.Session`
        """
        keypair = generate_key()
        csr = generate_csr(email, keypair)
        url = Endpoints.USER_CERTIFICATE.replace(":userId", email)
        csr_req = UserCsrRequest(csrPem=csr.decode("utf-8"))
        resp: UserCsrResponse = self.api.post(url, req_body=json.dumps(csr_req)).json()
        cert_chain_pem = resp["certChainPem"].encode("utf-8")
        auth = Auth(cert_chain_pem, keypair, email)
        return auth

    def create_session(
            self,
            attestation_specification: AttestationSpecification,
            auth: Auth,
            email: str,
    ) -> Session:
        """
        Creates a new `decentriq_platform.session.Session` instance to communicate
        with an enclave service with the specified identifier.

        Messages sent thorugh this session will be authenticated
        with the authentication object identifier specified during a call.
        """
        url = Endpoints.SESSIONS
        attestation_specification_hash = hashlib.sha256(attestation_specification.SerializeToString()).hexdigest()
        req_body = CreateSessionRequest(attestationSpecificationHash=attestation_specification_hash)
        response: SessionJsonResponse = self.api.post(
                url,
                json.dumps(req_body),
                {"Content-type": "application/json"}
        ).json()
        session = Session(
                self,
                response["sessionId"],
                attestation_specification,
                auth,
                email,
        )
        return session

    def _create_scope(self, email: str, metadata: Dict[str, str]) -> str:
        url = Endpoints.USER_SCOPES_COLLECTION.replace(":userId", email)
        req_body = CreateScopeRequest(metadata=metadata)
        response: ScopeJson = self.api.post(
                url,
                json.dumps(req_body),
                {"Content-type": "application/json"}
        ).json()
        return response["scopeId"]

    def _get_scope(self, email: str, scope_id: str) -> ScopeJson:
        url = Endpoints.USER_SCOPE \
                .replace(":userId", email) \
                .replace(":scopeId", scope_id)
        response: ScopeJson = self.api.get(url).json()
        return response

    def _get_scope_by_metadata(self, email: str, metadata: Dict[str, str]) -> Optional[str]:
        url = Endpoints.USER_SCOPES_COLLECTION.replace(":userId", email)
        response: List[ScopeJson] = self.api.get(
                url,
                params={"metadata": json.dumps(metadata)}
            ).json()
        if len(response) == 0:
            return None
        else:
            scope = response[0]
            return scope["scopeId"]

    def _ensure_scope_with_metadata(self, email: str, metadata: Dict[str, str]) -> str:
        scope = self._get_scope_by_metadata(email, metadata)
        if scope is None:
            scope = self._create_scope(email, metadata)
        return scope

    def _delete_scope(self, email: str, scope_id: str):
        url = Endpoints.USER_SCOPE \
            .replace(":userId", email) \
            .replace(":scopeId", scope_id)
        self.api.delete(url)

    def upload_file(
            self,
            email: str,
            file_input_stream: BinaryIO,
            description: str,
            key: Key,
            chunk_size: int = 8 * 1024 ** 2,
            parallel_uploads: int = 8
    ) -> bytes:
        """
        Uploads `file_input_stream` as a file usable by enclaves and returns the
        corresponding manifest hash

        **Parameters**:
        - `email`: owner of the file
        - `file_input_stream`: file content
        - `description`: file description
        - `key`: key used to encrypt the file
        """
        uploader = BoundedExecutor(
                bound=parallel_uploads * 2,
                max_workers=parallel_uploads
        )

        # create and upload chunks
        chunker = CsvChunker(file_input_stream, chunk_size=chunk_size)
        chunk_hashes: List[str] = []
        chunk_uploads_futures = []
        upload_description = self._create_upload(email)
        for chunk_hash, chunk_data in chunker:
            chunk_uploads_futures.append(
                uploader.submit(
                    self._encrypt_and_upload_chunk,
                    chunk_hash,
                    chunk_data,
                    key.material,
                    email,
                    upload_description["uploadId"]
                )
            )
            chunk_hashes.append(chunk_hash.hex())

        # check chunks uploads were successful
        completed, pending = futures.wait(
                chunk_uploads_futures,
                None,
                futures.FIRST_EXCEPTION
            )
        if len(pending):
            # re-raise exception
            for future in completed: future.result()
        uploader.shutdown(wait=False)

        # create manifest and upload
        manifest_hash, manifest_encrypted = create_encrypted_chunk(
                key.material,
                os.urandom(16),
                json.dumps(chunk_hashes).encode("utf-8")
        )
        scope_id = self._ensure_scope_with_metadata(email, {"type": ScopeTypes.USER_FILE})
        self._finalize_upload(
            user_id=email,
            scope_id=scope_id,
            upload_id=upload_description["uploadId"],
            name=description,
            manifest_hash=manifest_hash,
            manifest_encrypted=manifest_encrypted,
            chunks=chunk_hashes
        )
        return manifest_hash

    def _encrypt_and_upload_chunk(
            self,
            chunk_hash: bytes,
            chunk_data: bytes,
            key: bytes,
            user_id: str,
            upload_id: str
    ):
        cipher = StorageCipher(key)
        chunk_data_encrypted = cipher.encrypt(chunk_data)
        self._upload_chunk(chunk_hash, chunk_data_encrypted, user_id, upload_id)

    def _create_upload(self, user_id: str) -> UploadDescription:
        url = Endpoints.USER_UPLOADS_COLLECTION.replace(":userId", user_id)
        response = self.api.post(url, {}, {"Content-type": "application/json"})
        upload_description: UploadDescription = response.json()
        return upload_description

    def _upload_chunk(
            self,
            chunk_hash: bytes,
            chunk_data_encrypted: bytes,
            user_id: str,
            upload_id: str
    ):
        url = Endpoints.USER_UPLOAD_CHUNKS \
            .replace(":userId", user_id) \
            .replace(":uploadId", upload_id)
        wrapped_chunk= ChunkWrapper(
            hash=chunk_hash.hex(),
            data=b64encode(chunk_data_encrypted).decode("ascii")
        )
        self.api.post(url, json.dumps(wrapped_chunk), {"Content-type": "application/json"})

    def _delete_user_upload(self, email: str, upload_id: str):
        url = Endpoints.USER_UPLOAD \
            .replace(":userId", email) \
            .replace(":uploadId", upload_id)
        self.api.delete(url)

    def _get_user_upload(self, email: str, upload_id: str) -> UploadDescription:
        url = Endpoints.USER_UPLOAD.replace(
                ":userId", email
            ).replace(":uploadId", upload_id)
        response = self.api.get(url)
        return response.json()

    def _get_user_uploads_collection(self, email: str) -> List[UploadDescription]:
        url = Endpoints.USER_UPLOADS_COLLECTION.replace(":userId", email)
        response = self.api.get(url)
        return response.json()

    def _finalize_upload(
            self,
            user_id: str,
            scope_id: str,
            upload_id: str,
            name: str,
            manifest_hash: bytes,
            manifest_encrypted: bytes,
            chunks: List[str]
    ) -> FileDescription:
        url = Endpoints.USER_FILES_COLLECTION \
            .replace(":userId", user_id) \
            .replace(":scopeId", scope_id)
        payload = FinalizeUpload(
            uploadId=upload_id,
            manifest=b64encode(manifest_encrypted).decode("ascii"),
            manifestHash=manifest_hash.hex(),
            name=name,
            chunks=chunks
        )
        file_description: FileDescription = self.api.post(
            url,
            json.dumps(payload),
            {"Content-type": "application/json"}
        ).json()
        return file_description

    def delete_file(self, email: str, manifest_hash: bytes):
        """
        Deletes a user file from the decentriq platform
        """
        scope_id = self._ensure_scope_with_metadata(email, {"type": ScopeTypes.USER_FILE})
        url = Endpoints.USER_FILE \
            .replace(":userId", email) \
            .replace(":scopeId", scope_id) \
            .replace(":manifestHash", manifest_hash.hex())
        self.api.delete(url)

    def get_file(
            self,
            email: str,
            manifest_hash: bytes
    ) -> FileDescription:
        """
        Returns informations about a user file
        """
        scope_id = self._ensure_scope_with_metadata(email, {"type": ScopeTypes.USER_FILE})
        url = Endpoints.USER_FILE \
            .replace(":userId", email) \
            .replace(":scopeId", scope_id) \
            .replace(":manifestHash", manifest_hash.hex())
        response = self.api.get(url)
        return response.json()

    def get_files_collection(
            self,
            email: str,
    ) -> List[FileDescription]:
        """
        Returns the list of files uploaded by a user
        """
        scope_id = self._ensure_scope_with_metadata(email, {"type": ScopeTypes.USER_FILE})
        url = Endpoints.USER_FILES_COLLECTION \
            .replace(":userId", email) \
            .replace(":scopeId", scope_id)
        response = self.api.get(url)
        return response.json()



class BoundedExecutor:
    def __init__(self, bound, max_workers):
        self.executor = futures.ThreadPoolExecutor(max_workers=max_workers)
        self.semaphore = BoundedSemaphore(bound + max_workers)

    def submit(self, fn, *args, **kwargs):
        self.semaphore.acquire()
        try:
            future = self.executor.submit(fn, *args, **kwargs)
        except:
            self.semaphore.release()
            raise
        else:
            future.add_done_callback(lambda _: self.semaphore.release())
            return future

    def shutdown(self, wait=True):
        self.executor.shutdown(wait)
