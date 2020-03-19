from enum import Enum


class InBoundTol(Enum):
    LOWER_BOUND = 0
    UPPER_BOUND = 50


class CntSizeTol(Enum):
    LOWER_BOUND = 8600
    UPPER_BOUND = 150000
