from elasticsearch import Elasticsearch
import warnings
import argparse

warnings.filterwarnings("ignore")

index_name = "tmp2"
client = Elasticsearch(f"http://localhost:9200")

parser = argparse.ArgumentParser(description="Maps which are updated by the functions in the call graph of user-input function")
parser.add_argument("--func", required=True, help="Function name")

args = parser.parse_args()

def dfs(function_name, updateMaps_list):

    resp = client.search(index=index_name, pretty=True, source=["called_function_list", "updateMaps"], size=1000, query={
            "bool": {
                "must": {
                    "match_phrase": {
                    "funcName": function_name
                    }
                }
            }
        }).raw["hits"]["hits"][0]["_source"]

    content = resp["called_function_list"]
    updateMaps = resp['updateMaps']
    updateMaps_list += updateMaps
    for func in content:
        dfs(func, updateMaps_list)

WRITTEN_MAPS = []
dfs(args.func, WRITTEN_MAPS)
print(f"Maps written to throughout the FCG of function {args.func}")
print(WRITTEN_MAPS)