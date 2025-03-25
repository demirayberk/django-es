import abc
import math
from dataclasses import asdict
from typing import Any, Dict, Generic, Type, TypeVar

from elasticsearch import Elasticsearch

from core.settings import ES_HOST, ES_INDEX
from es.schemas import SearchResult

T = TypeVar("T")


class SingletonMeta(type):
    """Singleton implementation"""

    _instances: Dict[type, Any] = {}

    def __call__(cls, *args, **kwargs):  # pyright: ignore
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]  # pyright: ignore


class EsClient(metaclass=SingletonMeta):
    """I dont want to open connection everytime thats why singleton"""

    def __init__(self):
        self.es = Elasticsearch(ES_HOST)  # Initialize Elasticsearch connection
        self.index = ES_INDEX


class ElasticsearchBase(Generic[T], abc.ABC):
    """Scaleble base es class, even though we are using only one subclass here, just for showcase."""

    def __init__(self):
        self.__es_client = EsClient()  # Points to single client everytime

    @property
    @abc.abstractmethod
    def _dataclass_type(self) -> Type[T]: ...

    def insert(self, item: T, id: str = None, refresh: bool = False) -> Dict[str, Any]:

        document = asdict(item)
        return self.__es_client.es.index(
            index=self.__es_client.index, id=id, document=document, refresh=refresh
        )
    def search_wildcard(self, field: str, value: str, page: int = 1, page_size: int = 10) -> SearchResult[T]:

        from_ = (page - 1) * page_size
        es_query = {
            "query": {"wildcard": {f"{field}.keyword": {"value": f"{value}"}}},
            "from": from_,
            "size": page_size,
        }

        response = self.__es_client.es.search(
            index=self.__es_client.index, body=es_query
        )
        total = response["hits"]["total"]["value"]
        total_pages = math.ceil(total / page_size)

        return SearchResult(
            total= total,
            hits=[
                self._dataclass_type(**hit["_source"])
                for hit in response["hits"]["hits"]
            ],
            page = page,
            page_size = page_size,
            total_pages = total_pages
        )
