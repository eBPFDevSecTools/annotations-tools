from elasticsearch import Elasticsearch
import warnings
import argparse

warnings.filterwarnings("ignore")

index_name = "tmp2"
client = Elasticsearch(f"http://localhost:9200")

parser = argparse.ArgumentParser(description="Maps used in a user-input repository")
parser.add_argument("--repo", required=True, help="Name of the Repository")

args = parser.parse_args()

resp = client.search(index=index_name, pretty=True, source=["readMaps", "updateMaps"], size=1000, query={
            "fuzzy": {
                "File": args.repo
            }
        })

hits = resp.raw['hits']['hits']

maps = []
for dic in hits:
    maps += list(map(lambda x: x.strip(), dic["_source"]["readMaps"]))
    maps += list(map(lambda x: x.strip(), dic["_source"]["updateMaps"]))

maps = set(maps)
print(f"List of Maps - {maps}")
counts = len(maps)
print(f"Number of Maps - {counts}")