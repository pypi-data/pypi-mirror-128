from typing import List

from .common import to_typed_message, Inbound
from .v2grpc.v2ray.com.core.common.protocol import user_pb2 as user_pb
from .v2grpc.v2ray.com.core.proxy.vmess import account_pb2
from .v2grpc.v2ray.com.core.proxy.vmess.inbound import config_pb2 as vmess_pb


# v2ray.core.common.protocol.User
class User:
    def __init__(self, uuid: str, email: str, alter_id: int = 4, level: int = 0):
        self.id = uuid
        self.email = email
        self.alter_id = alter_id
        self.level = level

    def to_user_proto(self):
        return user_pb.User(
            level=self.level,
            email=self.email,
            account=to_typed_message(account_pb2.Account(
                id=self.id,
                alter_id=self.alter_id
            ))
        )


class VmessInbound(Inbound):
    def __init__(self, alter_id: int = 4, level: int = 0):
        self.alter_id = alter_id
        self.level = level
        self._user = []  # type:List[User]

    def add_user(self, user: User):
        self._user.append(user)

    def to_message(self):
        return to_typed_message(
            vmess_pb.Config(
                user=[u.to_user_proto() for u in self._user],
                default=vmess_pb.DefaultConfig(alter_id=self.alter_id, level=self.level)
            )
        )


