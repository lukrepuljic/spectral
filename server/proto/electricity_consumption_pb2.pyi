from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ConsumptionPoint(_message.Message):
    __slots__ = ["measurement", "time"]
    MEASUREMENT_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    measurement: float
    time: str
    def __init__(self, time: _Optional[str] = ..., measurement: _Optional[float] = ...) -> None: ...

class Request(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...
