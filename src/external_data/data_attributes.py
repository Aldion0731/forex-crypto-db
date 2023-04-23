from enum import Enum


class DataAttributes(str, Enum):
    date = "date"
    open = "open"
    high = "high"
    low = "low"
    close = "close"
    volume = "volume"
