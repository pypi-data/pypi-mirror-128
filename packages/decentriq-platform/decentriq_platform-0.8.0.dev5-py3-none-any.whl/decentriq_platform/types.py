from .proto.attestation_pb2 import AttestationSpecification
from typing import List, Dict
from typing_extensions import TypedDict
from enum import Enum

__all__ = ["FileDescription"]

class ScopeTypes(str, Enum):
    USER_FILE = "user_file",
    DATA_ROOM_DEFINITION = "dataroom_definition",
    DATA_ROOM_INTERMEDIATE_DATA = "dataroom_intermediate_data"


class UserResponse(TypedDict):
    id: str
    email: str


class UserCsrRequest(TypedDict):
    csrPem: str


class UserCsrResponse(TypedDict):
    certChainPem: str


class SystemCaResponse(TypedDict):
    rootCertificate: str


class CreateSessionRequest(TypedDict):
    attestationSpecificationHash: str


class SessionJsonResponse(TypedDict):
    sessionId: str
    attestationSpecificationHash: str


class FinalizeUpload(TypedDict):
    uploadId: str
    manifest: str
    name: str
    manifestHash: str
    chunks: List[str]


class ChunkWrapper(TypedDict):
    hash: str
    data: str


class UploadDescription(TypedDict):
    uploadId: str


class ChunkDescription(TypedDict):
    chunkHash: str


class DataRoomDescription(TypedDict):
    dataRoomId: str
    tableName: str


class PartialFileDescription(TypedDict):
    dataRoomIds: List[DataRoomDescription]


class FileDescription(TypedDict):
    """
    This class includes information about an uploaded dataset
    """
    manifestHash: str
    filename: str
    chunks: List[ChunkDescription]
    dataRoomIds: List[DataRoomDescription]


class SignatureResponse(TypedDict):
    type: str
    data: List[int]


class EnclaveMessage(TypedDict):
    data: str


class FatquoteResBody(TypedDict):
    fatquoteBase64: str


class DatasetManifestMetadata(TypedDict):
    name: str
    manifestHash: str
    chunks: List[str]


class AttestationSpec(TypedDict):
    name: str
    version: str
    proto: AttestationSpecification


class CreateScopeRequest(TypedDict):
    metadata: Dict[str, str]


class ScopeJson(TypedDict):
    scopeId: str
    metadata: Dict[str, str]


class AttestationSpecJson(TypedDict):
    name: str
    version: str
    spec: str


class AttestationSpecsResponse(TypedDict):
    attestationSpecs: List[AttestationSpecJson]


class Tcb(TypedDict):
    sgxtcbcomp01svn: int
    sgxtcbcomp02svn: int
    sgxtcbcomp03svn: int
    sgxtcbcomp04svn: int
    sgxtcbcomp05svn: int
    sgxtcbcomp06svn: int
    sgxtcbcomp07svn: int
    sgxtcbcomp08svn: int
    sgxtcbcomp09svn: int
    sgxtcbcomp10svn: int
    sgxtcbcomp11svn: int
    sgxtcbcomp12svn: int
    sgxtcbcomp13svn: int
    sgxtcbcomp14svn: int
    sgxtcbcomp15svn: int
    sgxtcbcomp16svn: int


class TcbLevel(TypedDict):
    tcb: Tcb
    tcbStatus: str


class TcbInfo(TypedDict):
    version: int
    issueDate: str
    nextUpdate: str
    fmspc: str
    pceId: str
    tcbType: int
    tcbEvaluationDataNumber: int
    tcbLevels: List[TcbLevel]


class TcbInfoContainer(TypedDict):
    tcbInfo: TcbInfo
    signature: str


class IasResponse(TypedDict):
    isvEnclaveQuoteBody: str
    isvEnclaveQuoteStatus: str
