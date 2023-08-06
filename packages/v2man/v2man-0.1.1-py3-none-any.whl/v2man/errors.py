class V2ManError(Exception):
    """V2Man base exception"""

    def __init__(self, details):
        self.details = details


class UserExistsError(V2ManError):
    """The user specified by the email already exist"""

    def __init__(self, details, email: str):
        self.email = email
        self.details = details


class UserNotFoundError(V2ManError):
    """The user specified by the email does not exist"""

    def __init__(self, details, email: str):
        self.email = email
        self.details = details


class InboundNotFoundError(V2ManError):
    """The inbound does not exist"""
    def __init__(self, details, inbound_tag: str):
        self.inbound_tag = inbound_tag
        self.details = details


class AddressAlreadyInUseError(V2ManError):
    """Address already in use"""
    def __init__(self, details, port):
        self.port = port
        self.details = details
