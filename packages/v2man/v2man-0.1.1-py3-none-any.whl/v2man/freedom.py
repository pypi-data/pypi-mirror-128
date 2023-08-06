from .common import Outbound, Network, to_typed_message
from .v2grpc.v2ray.com.core.common.net import address_pb2
from .v2grpc.v2ray.com.core.common.protocol import server_spec_pb2
from .v2grpc.v2ray.com.core.proxy.freedom import config_pb2 as freedom_pb2


class Strategy:
    AsIs = "AS_IS"
    IP = "USE_IP"
    IPv4 = "USE_IP4"
    IPv6 = "USE_IP6"


class FreedomOutbound(Outbound):
    def __init__(self, redirect: Network = None, strategy: Strategy = Strategy.AsIs, level: int = 0):
        self.strategy = strategy
        self.level = level
        if redirect is None:
            self.redirect = None
        else:
            self.redirect = server_spec_pb2.ServerEndpoint(
                address=address_pb2.IPOrDomain(
                    ip=self.ip2bytes(redirect.address),
                ),
                port=redirect.port,
            )

    def to_typed_message(self):
        return to_typed_message(
            freedom_pb2.Config(
                domain_strategy=self.strategy,
                user_level=self.level,
                destination_override=self.redirect
            )
        )

    def ip2bytes(self, address: str):
        # todo: support ipv6
        return bytes([int(i) for i in address.split('.')])
