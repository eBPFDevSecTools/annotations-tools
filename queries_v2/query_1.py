from elasticsearch import Elasticsearch
import warnings
import argparse

warnings.filterwarnings("ignore")

index_name = "tmp3"
client = Elasticsearch(f"http://localhost:9200")

parser = argparse.ArgumentParser(description="Finding the functions which call the user-input bpf helper")
parser.add_argument("--helper", required=True, help="BPF Helper Name")

args = parser.parse_args()

resp = client.search(index=index_name, pretty=True, source=["File", "funcName"], size=1000, query={
            "match": {
                "helper": args.helper
            }
        })

hits = resp.raw['hits']['hits']

ls = []
filenames = []
for dic in hits:
    ls.append(dic["_source"]["funcName"])
    filenames.append(dic["_source"]["File"])

ls = set(ls)
filenames = set(filenames)
print(f"List of Functions - {ls}")
print(f"File names of functions - {filenames}")
counts = len(ls)
print(f"Number of Functions - {counts}")
