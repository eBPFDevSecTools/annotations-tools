from elasticsearch import Elasticsearch
import warnings
import argparse

warnings.filterwarnings("ignore")

index_name = "tmp3"
client = Elasticsearch(f"http://localhost:9200")

parser = argparse.ArgumentParser(description="Functions with a user-input field wose value is the user-input value")
parser.add_argument("--field", required=True, help="Name of the field")
parser.add_argument("--value", required=True, help="Value")

args = parser.parse_args()

resp = client.search(index=index_name, pretty=True, source=["funcName"], size=1000, query={
            "match": {
                args.field : args.value
            }
        })

hits = resp.raw['hits']['hits']

funcs = set()
for dic in hits:
    funcs.add(dic["_source"]["funcName"])

print(f"List of Functions - {funcs}")
counts = len(funcs)
print(f"Number of Functions - {counts}")