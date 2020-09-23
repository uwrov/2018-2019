from enum import Enum


class InBoundTol(Enum):
    LOWER_BOUND = 0
    UPPER_BOUND = 50


class CntSizeTol(Enum):
    LOWER_BOUND = 15000
    UPPER_BOUND = 150000
