from django.core.management.base import BaseCommand
from es.es_base import EsClient

from core.settings import ES_INDEX

class Command(BaseCommand):
    help = "Creates the octoxlabsdata index in Elasticsearch with the specified mapping and inserts mock data"

    def handle(self, *args, **kwargs): # pyright: ignore
        index_name = ES_INDEX

        es = EsClient().es

        mapping = {
            "properties": {
                "Hostname": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "Ip": {
                    "type": "ip"
                }
            }
        }

        # Create the index if it doesn't exist
        if not es.indices.exists(index=index_name):
            self.stdout.write(self.style.SUCCESS(f"Index '{index_name}' does not exist. Creating index..."))
            es.indices.create(index=index_name, body={"mappings": mapping})
            self.stdout.write(self.style.SUCCESS(f"Index '{index_name}' created successfully!"))
        else:
            self.stdout.write(self.style.WARNING(f"Index '{index_name}' already exists."))

        mock_data = [
            {"Hostname": "octoxlabs01", "Ip": ["0.0.0.0"]},
            {"Hostname": "octoxlabs02", "Ip": ["192.168.0.1"]},
            {"Hostname": "octoxlabs03", "Ip": ["10.0.0.1"]},
            {"Hostname": "octoxlabs04", "Ip": ["172.16.0.1"]},
            {"Hostname": "octoxlabs05", "Ip": ["192.168.1.1"]},
            {"Hostname": "octoxlabs06", "Ip": ["10.0.0.2"]},
            {"Hostname": "octoxlabs07", "Ip": ["172.16.1.1"]},
            {"Hostname": "octoxlabs08", "Ip": ["192.168.2.1"]},
            {"Hostname": "octoxlabs09", "Ip": ["10.0.1.1"]},
            {"Hostname": "octoxlabs10", "Ip": ["172.16.2.1"]},
        ]

        # Insert mock data into the index
        for i, data in enumerate(mock_data, start=1):
            try:
                es.index(index=index_name, id=str(i), document=data)
                self.stdout.write(self.style.SUCCESS(f"Inserted document {i} with data: {data}"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Failed to insert document {i}: {e}"))
