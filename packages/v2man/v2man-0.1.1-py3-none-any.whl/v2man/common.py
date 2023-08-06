from .v2grpc.v2ray.com.core.common.serial import typed_message_pb2 as typed_message


def to_typed_message(message):
    return typed_message.TypedMessage(
        type=message.DESCRIPTOR.full_name,
        value=message.SerializeToString()
    )


class Inbound:
    def to_message(self):
        return None


class Outbound:
    def to_typed_message(self):
        return None


class Network:
    def __init__(self, address: str, port: int):
        self.port = port
        self.address = address
