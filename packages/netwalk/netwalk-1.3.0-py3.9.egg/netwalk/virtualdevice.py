"""Define Virtual Device class"""

from typing import Dict
from .interface import Interface

class VirtualDevice():
    def __init__(self) -> None:
        pass

class Stack(VirtualDevice):
    members: Dict[int, str]
    interfaces = Dict[str, Interface]

    def __init__(self) -> None:
        super().__init__()
