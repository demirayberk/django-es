from es.es_base import ElasticsearchBase
from es.schemas import HostNameMapping




class HostIpSearch(ElasticsearchBase[HostNameMapping]):
    """Subclass of ElasticSearchBase"""

    @property
    def _dataclass_type(self):
        return HostNameMapping
