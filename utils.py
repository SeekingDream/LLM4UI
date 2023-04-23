from enum import Enum, unique


@unique
class ErrorReason(Enum):
    NoSuchElementError = 0
    AttributeError = 1
    Other = 2