from elasticsearch import Elasticsearch
import warnings
import argparse

warnings.filterwarnings("ignore")

index_name = "tmp3"
client = Elasticsearch(f"http://localhost:9200")

parser = argparse.ArgumentParser(description="Functions from a user-input repository writing to a user-input map")
parser.add_argument("--repo", required=True, help='Name of the repository')
parser.add_argument("--map", required=True, help="Name of the BPF map")

args = parser.parse_args()

resp = client.search(index=index_name, pretty=True, source=["funcName"], size=1000, query={
            "bool": {
                "filter": {
                    "match_phrase": {
                    "File": args.repo
                    }
                },
                "must": {
                    "match_phrase": {
                    "updateMaps": args.map
                    }
                }
            }
        })

hits = resp.raw['hits']['hits']

funcs = set()
for dic in hits:
    funcs.add(dic["_source"]["funcName"])

print(f"List of Functions - {funcs}")
counts = len(funcs)
print(f"Number of Functions - {counts}")