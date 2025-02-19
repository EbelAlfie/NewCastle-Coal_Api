from enum import Enum

class ConnectionStatus(Enum):
    Connecting = "connecting"
    Connected = "connected"
    Disconnected = "disconnected"