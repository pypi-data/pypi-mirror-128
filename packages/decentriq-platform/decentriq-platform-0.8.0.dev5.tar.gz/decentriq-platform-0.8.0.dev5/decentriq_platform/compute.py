from .proto.length_delimited import serialize_length_delimited
from .proto.gcg_pb2 import DriverTaskConfig, NoopConfig

class Noop():
    """
    Computation node which does not perform any operation and produces an empty
    output. This is mostly used to allow users to test the execution of other computation
    nodes without giving access to the results.
    """
    config: bytes

    def __init__(self) -> None:
        self.config = serialize_length_delimited(DriverTaskConfig(noop=NoopConfig()))

