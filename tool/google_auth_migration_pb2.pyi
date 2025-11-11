from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Algorithm(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALGORITHM_TYPE_UNSPECIFIED: _ClassVar[Algorithm]
    SHA1: _ClassVar[Algorithm]
    SHA256: _ClassVar[Algorithm]
    SHA512: _ClassVar[Algorithm]
    MD5: _ClassVar[Algorithm]

class DigitCount(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DIGIT_COUNT_UNSPECIFIED: _ClassVar[DigitCount]
    SIX: _ClassVar[DigitCount]
    EIGHT: _ClassVar[DigitCount]

class OtpType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OTP_TYPE_UNSPECIFIED: _ClassVar[OtpType]
    HOTP: _ClassVar[OtpType]
    TOTP: _ClassVar[OtpType]
ALGORITHM_TYPE_UNSPECIFIED: Algorithm
SHA1: Algorithm
SHA256: Algorithm
SHA512: Algorithm
MD5: Algorithm
DIGIT_COUNT_UNSPECIFIED: DigitCount
SIX: DigitCount
EIGHT: DigitCount
OTP_TYPE_UNSPECIFIED: OtpType
HOTP: OtpType
TOTP: OtpType

class MigrationPayload(_message.Message):
    __slots__ = ("otp_parameters", "version", "batch_size", "batch_index", "batch_id")
    OTP_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    BATCH_INDEX_FIELD_NUMBER: _ClassVar[int]
    BATCH_ID_FIELD_NUMBER: _ClassVar[int]
    otp_parameters: _containers.RepeatedCompositeFieldContainer[OtpParameters]
    version: int
    batch_size: int
    batch_index: int
    batch_id: int
    def __init__(self, otp_parameters: _Optional[_Iterable[_Union[OtpParameters, _Mapping]]] = ..., version: _Optional[int] = ..., batch_size: _Optional[int] = ..., batch_index: _Optional[int] = ..., batch_id: _Optional[int] = ...) -> None: ...

class OtpParameters(_message.Message):
    __slots__ = ("secret", "name", "issuer", "algorithm", "digits", "type", "counter")
    SECRET_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ISSUER_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    DIGITS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    COUNTER_FIELD_NUMBER: _ClassVar[int]
    secret: bytes
    name: str
    issuer: str
    algorithm: Algorithm
    digits: DigitCount
    type: OtpType
    counter: int
    def __init__(self, secret: _Optional[bytes] = ..., name: _Optional[str] = ..., issuer: _Optional[str] = ..., algorithm: _Optional[_Union[Algorithm, str]] = ..., digits: _Optional[_Union[DigitCount, str]] = ..., type: _Optional[_Union[OtpType, str]] = ..., counter: _Optional[int] = ...) -> None: ...
