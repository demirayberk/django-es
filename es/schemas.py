from typing import TypeVar, Generic, List, Text
from dataclasses import dataclass



T = TypeVar("T")

@dataclass
class HostNameMapping:
    Hostname: str
    Ip: List[Text]

@dataclass
class SearchResult(Generic[T]):
    """Generic Search Class"""
    total: int
    hits: List[T]
