from .common import to_typed_message
from .v2grpc.v2ray.com.core.transport.internet import config_pb2 as internet_config_pb2
from .v2grpc.v2ray.com.core.transport.internet.headers.noop import config_pb2 as noop_pb2
from .v2grpc.v2ray.com.core.transport.internet.headers.srtp import config_pb2 as srtp_pb2
from .v2grpc.v2ray.com.core.transport.internet.headers.tls import config_pb2 as dtls_pb2
from .v2grpc.v2ray.com.core.transport.internet.headers.utp import config_pb2 as utp_pb2
from .v2grpc.v2ray.com.core.transport.internet.headers.wechat import config_pb2 as wechat_pb2
from .v2grpc.v2ray.com.core.transport.internet.headers.wireguard import config_pb2 as wireguard_pb2
from .v2grpc.v2ray.com.core.transport.internet.kcp import config_pb2 as kcp_config_pb2
from .v2grpc.v2ray.com.core.transport.internet.websocket import config_pb2 as websocket_config_pb2


class Stream:
    def to_stream_config_message(self):
        pass


class Websocket(Stream):
    def __init__(self, path="/", headers=None):
        super(Websocket, self).__init__()
        if headers is None:
            headers = {}
        self.path = path
        self._header = []
        for key, val in headers.items():
            self._header.append(websocket_config_pb2.Header(
                key=key,
                value=val,
            ))

    def to_stream_config_message(self):
        return internet_config_pb2.StreamConfig(
            protocol_name="ws",
            transport_settings=[
                internet_config_pb2.TransportConfig(
                    protocol_name="ws",
                    settings=to_typed_message(
                        websocket_config_pb2.Config(
                            path=self.path,
                            header=self._header
                        )
                    )
                )
            ]
        )


class KcpHeader:
    WeChat = wechat_pb2.VideoConfig()
    Utp = utp_pb2.Config()
    Srtp = srtp_pb2.Config()
    Dtls = dtls_pb2.PacketConfig()
    Wireguard = wireguard_pb2.WireguardConfig()
    Noop = noop_pb2.Config()


class Kcp(Stream):
    def __init__(self, header: KcpHeader = KcpHeader.Noop, tti: int = 50, read_buffer=2 * 1024 * 1024,
                 write_buffer=2 * 1024 * 1024, uplink_capacity=20, downlink_capacity=20):
        super(Kcp, self).__init__()
        self.stream = internet_config_pb2.StreamConfig(
            protocol=internet_config_pb2.MKCP,
            transport_settings=[
                internet_config_pb2.TransportConfig(
                    protocol=internet_config_pb2.MKCP,
                    settings=to_typed_message(
                        kcp_config_pb2.Config(
                            tti=tti,
                            uplink_capacity=uplink_capacity,
                            downlink_capacity=downlink_capacity,
                            write_buffer=write_buffer,
                            read_buffer=read_buffer,
                            congestion=True,
                            header_config=to_typed_message(header)
                        )
                    )
                )
            ]
        )

    def to_stream_config_message(self):
        return self.stream
