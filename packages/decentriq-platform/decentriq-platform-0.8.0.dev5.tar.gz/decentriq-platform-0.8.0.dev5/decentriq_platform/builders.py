from __future__ import annotations
from typing import List
from .proto.data_room_pb2 import (
    AuthenticationMethod, UserPermission, ComputeNode,
    ComputeNodeLeaf, ComputeNodeBranch, Permission, DataRoom
)
from .proto.attestation_pb2 import (AttestationSpecification)
import random

__all__ = ["DataRoomBuilder"]


class DataRoomBuilder():
    """
    An helper class to ease the building process of a data clean room
    """
    attestationSpecifications: List[AttestationSpecification]
    authenticationMethods: List[AuthenticationMethod]
    userPermissions: List[UserPermission]
    computeNodes: List[ComputeNode]
    id: str

    def __init__(self) -> None:
        self.attestationSpecifications = list()
        self.authenticationMethods = list()
        self.userPermissions = list()
        self.computeNodes = list()
        self.id = random.getrandbits(64).to_bytes(8, byteorder='little').hex()

    def add_leaf_node(self, name: str, is_required=False) -> None:
        """
        Add a new leaf node. If the node is marked as required, any computation
        which includes it as a dependency will not progress.
        """
        node = ComputeNode(
            nodeName=name,
            leaf=ComputeNodeLeaf(isRequired=is_required)
        )
        self.computeNodes.append(node)

    def add_compute_node(
            self,
            name: str,
            config: bytes,
            attestation: AttestationSpecification,
            dependencies: List[str]
    ) -> None:
        """
        Add a new compute node. The configuration for a compute node should be
        created using one of the compute-specific libraries.
        """
        try:
            attestation_index = self.attestationSpecifications.index(attestation)
        except ValueError:
            self.attestationSpecifications.append(attestation)
            attestation_index = len(self.attestationSpecifications) - 1
        node = ComputeNode(
            nodeName=name,
            branch=ComputeNodeBranch(
                config=config,
                attestationSpecificationIndex=attestation_index,
                dependencies=dependencies,
            )
        )
        self.computeNodes.append(node)

    def add_user_permission(
            self,
            email: str,
            authentication_method: AuthenticationMethod,
            permissions: List[Permission],
    ) -> None:
        """
        Add permissions for a user. The authentication is performed on the enclave side
        based on the method supplied.
        """
        try:
            authentication_method_index = self.authenticationMethods.index(authentication_method)
        except ValueError:
            self.authenticationMethods.append(authentication_method)
            authentication_method_index = len(self.authenticationMethods) - 1

        permission = UserPermission(
            email=email,
            authenticationMethodIndex=authentication_method_index,
            permissions=permissions
        )
        self.userPermissions.append(permission)

    def set_id(
            self,
            id: str,
    ) -> None:
        """
        Set identifier for the DataRoom. This is not used for addressing the dataroom.
        """
        self.id = id


    def build(self) -> DataRoom:
        """
        Finalize data room contruction
        """
        data_room = DataRoom()
        data_room.computeNodes.extend(self.computeNodes)
        data_room.attestationSpecifications.extend(self.attestationSpecifications)
        data_room.userPermissions.extend(self.userPermissions)
        data_room.authenticationMethods.extend(self.authenticationMethods)
        data_room.id = self.id
        return data_room
