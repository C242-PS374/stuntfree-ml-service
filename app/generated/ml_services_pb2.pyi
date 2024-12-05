from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ImageRequest(_message.Message):
    __slots__ = ("image_data",)
    IMAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    image_data: bytes
    def __init__(self, image_data: _Optional[bytes] = ...) -> None: ...

class ImageResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: str
    def __init__(self, result: _Optional[str] = ...) -> None: ...

class NutritionRequest(_message.Message):
    __slots__ = ("height", "weight", "age")
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    height: float
    weight: float
    age: int
    def __init__(self, height: _Optional[float] = ..., weight: _Optional[float] = ..., age: _Optional[int] = ...) -> None: ...

class NutritionResponse(_message.Message):
    __slots__ = ("nutrition_status",)
    NUTRITION_STATUS_FIELD_NUMBER: _ClassVar[int]
    nutrition_status: str
    def __init__(self, nutrition_status: _Optional[str] = ...) -> None: ...

class StuntingRequest(_message.Message):
    __slots__ = ("age", "birth_weight", "birth_length", "body_weight", "body_length", "is_sanitized_place", "is_healthy_food")
    AGE_FIELD_NUMBER: _ClassVar[int]
    BIRTH_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    BIRTH_LENGTH_FIELD_NUMBER: _ClassVar[int]
    BODY_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    BODY_LENGTH_FIELD_NUMBER: _ClassVar[int]
    IS_SANITIZED_PLACE_FIELD_NUMBER: _ClassVar[int]
    IS_HEALTHY_FOOD_FIELD_NUMBER: _ClassVar[int]
    age: int
    birth_weight: float
    birth_length: int
    body_weight: float
    body_length: float
    is_sanitized_place: int
    is_healthy_food: int
    def __init__(self, age: _Optional[int] = ..., birth_weight: _Optional[float] = ..., birth_length: _Optional[int] = ..., body_weight: _Optional[float] = ..., body_length: _Optional[float] = ..., is_sanitized_place: _Optional[int] = ..., is_healthy_food: _Optional[int] = ...) -> None: ...

class StuntingResponse(_message.Message):
    __slots__ = ("stunting_status",)
    STUNTING_STATUS_FIELD_NUMBER: _ClassVar[int]
    stunting_status: str
    def __init__(self, stunting_status: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class HealthResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...
