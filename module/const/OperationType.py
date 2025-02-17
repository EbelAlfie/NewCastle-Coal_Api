from enum import Enum

class OperationType(Enum):
    Open = "open"
    Close = "close"
    Ping = "ping"
    Pong = "pong"
    Message = "message"
    Error = "error"
    Noop = "noop"
