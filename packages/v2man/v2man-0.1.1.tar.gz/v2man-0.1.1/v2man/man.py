import grpc

from .common import to_typed_message, Inbound, Outbound
from .errors import *
from .stream import Stream
from .v2grpc import proxyman_pb2_grpc
from .v2grpc import stats_pb2_grpc
from .v2grpc.v2ray.com.core import config_pb2 as core_config_pb
from .v2grpc.v2ray.com.core.app.proxyman import config_pb2 as proxyman_config_pb
from .v2grpc.v2ray.com.core.app.proxyman.command import command_pb2 as proxyman_pb
from .v2grpc.v2ray.com.core.app.stats.command import command_pb2 as stats_pb
from .v2grpc.v2ray.com.core.common.net import address_pb2
from .v2grpc.v2ray.com.core.common.net import port_pb2
from .v2grpc.v2ray.com.core.common.protocol import user_pb2 as user_pb
from .v2grpc.v2ray.com.core.proxy.vmess import account_pb2 as account_pb
from .v2grpc.v2ray.com.core.transport.internet.config_pb2 import ProxyConfig


class UserStats:
    def __init__(self, email: str):
        self.email = email
        self.uplink = 0
        self.downlink = 0

    def __str__(self):
        return "%s: ↑ %s | ↓ %s" % (self.email, self.uplink, self.downlink)


class Receiver:
    def __init__(self, port: int, address: str, stream: Stream = None):
        self.port = port
        self.address = address
        if stream is None:
            self.stream = Stream()
        else:
            self.stream = stream

    def to_message(self):
        return to_typed_message(
            proxyman_config_pb.ReceiverConfig(
                port_range=port_pb2.PortRange(
                    From=self.port,
                    To=self.port
                ),
                listen=address_pb2.IPOrDomain(
                    ip=self.ip2bytes()
                ),
                allocation_strategy=None,
                stream_settings=self.stream.to_stream_config_message(),
                receive_original_destination=None,
                domain_override=None,
                sniffing_settings=None
            )
        )

    def ip2bytes(self):
        # todo: support ipv6
        return bytes([int(i) for i in self.address.split('.')])


class Sender:
    def __init__(self, send_through: str = "0.0.0.0", stream: Stream = None, proxy_tag: str = None):
        """
        :param send_through:The IP address for sending traffic out. Default 0.0.0.0
        :param stream: Low-level transport stream settings.
        :param proxy_tag: Configuration for delegating traffic from this outbound to another. When this is set,
                            streamSettings of this outbound will has no effect.
        """
        self.address = send_through
        if stream is None:
            self.stream = Stream()
        else:
            self.stream = stream
        if proxy_tag is None:
            self.proxy = None
        else:
            self.proxy = ProxyConfig(tag=proxy_tag)

    def to_typed_message(self):
        return to_typed_message(
            proxyman_config_pb.SenderConfig(
                via=address_pb2.IPOrDomain(ip=self.ip2bytes()),
                stream_settings=self.stream.to_stream_config_message(),
                proxy_settings=self.proxy,
            )
        )

    def ip2bytes(self):
        # todo: support ipv6
        return bytes([int(i) for i in self.address.split('.')])


class Manager:
    def __init__(self, grpc_addr: str):
        self._channel = grpc.insecure_channel(grpc_addr)
        self._stats_stub = stats_pb2_grpc.StatsServiceStub(self._channel)
        self._proxy_stub = proxyman_pb2_grpc.HandlerServiceStub(self._channel)

    def add_inbound(self, tag: str, receiver: Receiver, inbound: Inbound):
        req = proxyman_pb.AddInboundRequest(
            inbound=core_config_pb.InboundHandlerConfig(
                tag=tag,
                receiver_settings=receiver.to_message(),
                proxy_settings=inbound.to_message(),
            )
        )
        try:
            self._proxy_stub.AddInbound(req)
        except grpc.RpcError as e:
            if isinstance(e, grpc.Call):
                details = e.details()
                if details.endswith("address already in use"):
                    raise AddressAlreadyInUseError(details, 0)
            raise V2ManError(e)

    def remove_inbound(self, tag: str):
        try:
            self._proxy_stub.RemoveInbound(proxyman_pb.RemoveInboundRequest(
                tag=tag
            ))
        except grpc.RpcError as e:
            if isinstance(e, grpc.Call):
                details = e.details()
                if details.endswith("not enough information for making a decision"):
                    raise InboundNotFoundError(details, tag)
            raise V2ManError(e)

    def add_outbound(self, tag: str, sender: Sender, outbound: Outbound):
        req = proxyman_pb.AddOutboundRequest(
            outbound=core_config_pb.OutboundHandlerConfig(
                tag=tag,
                sender_settings=sender.to_typed_message(),
                proxy_settings=outbound.to_typed_message(),
            )
        )
        try:
            self._proxy_stub.AddOutbound(req)
        except grpc.RpcError as e:
            raise V2ManError(e)

    def remove_outbound(self, tag: str):
        try:
            self._proxy_stub.RemoveOutbound(proxyman_pb.RemoveOutboundRequest(
                tag=tag
            ))
        except grpc.RpcError as e:
            if isinstance(e, grpc.Call):
                details = e.details()
                if details.endswith("not enough information for making a decision"):
                    raise InboundNotFoundError(details, tag)
            raise V2ManError(e)

    def stats_sys(self):
        try:
            resp = self._stats_stub.GetSysStats(stats_pb.SysStatsRequest())  # type:stats_pb.SysStatsResponse
            return resp
        except grpc.RpcError as e:
            raise V2ManError(e)

    def stats_user(self, email: str, reset: bool = True):
        uplink_query = f"user>>>{email}>>>traffic>>>uplink"
        downlink_query = f"user>>>{email}>>>traffic>>>downlink"
        req = stats_pb.QueryStatsRequest(pattern=f"user>>>{email}>>>traffic", reset=reset)
        ret = self._stats_stub.QueryStats(req)  # type: stats_pb.QueryStatsResponse
        user_stats = UserStats(email)

        for stat in ret.stat:
            if stat.name.endswith("uplink"):
                user_stats.uplink = stat.value
            else:
                user_stats.downlink = stat.value
        return user_stats

    def add_user(self, tag: str, email: str, uuid: str, level: int = 0, alter_id: int = 64):
        req = proxyman_pb.AlterInboundRequest(
            tag=tag,
            operation=to_typed_message(
                proxyman_pb.AddUserOperation(
                    user=user_pb.User(
                        level=level,
                        email=email,
                        account=to_typed_message(account_pb.Account(
                            id=uuid,
                            alter_id=alter_id
                        ))
                    )
                )
            )
        )
        try:
            self._proxy_stub.AlterInbound(req)
        except grpc.RpcError as e:
            if isinstance(e, grpc.Call):
                details = e.details()  # type:str
                if details.endswith("already exists."):
                    raise UserExistsError(details, email)
                if details.endswith(f"handler not found: {tag}"):
                    raise InboundNotFoundError(details, tag)
            raise V2ManError(e)

    def remove_user(self, tag: str, email: str):
        req = proxyman_pb.AlterInboundRequest(
            tag=tag,
            operation=to_typed_message(
                proxyman_pb.RemoveUserOperation(
                    email=email
                )
            )
        )
        try:
            self._proxy_stub.AlterInbound(req)
        except grpc.RpcError as e:
            if isinstance(e, grpc.Call):
                details = e.details()
                if details.endswith("not found."):
                    raise UserNotFoundError(details, email)
                elif details.endswith(f"handler not found: {tag}"):
                    raise InboundNotFoundError(details, tag)
            raise V2ManError(e)
