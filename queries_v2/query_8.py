from elasticsearch import Elasticsearch
import warnings
import argparse

warnings.filterwarnings("ignore")

index_name = "tmp3"
client = Elasticsearch(f"http://localhost:9200")

parser = argparse.ArgumentParser(description="Maps read by all the functions in the call graph of the user-input function")
parser.add_argument("--func", required=True, help="Function name")

args = parser.parse_args()

def dfs(function_name, readMaps_list):

    resp = client.search(index=index_name, pretty=True, source=["called_function_list", "readMaps"], size=1000, query={
            "bool": {
                "must": {
                    "match_phrase": {
                    "funcName": function_name
                    }
                }
            }
        }).raw["hits"]["hits"][0]["_source"]

    content = resp["called_function_list"]
    readMaps = resp['readMaps']
    readMaps_list += readMaps
    for func in content:
        dfs(func, readMaps_list)

READMAPS = []
dfs(args.func, READMAPS)
print(f"Maps read throughout the FCG of function {args.func}")
print(READMAPS)