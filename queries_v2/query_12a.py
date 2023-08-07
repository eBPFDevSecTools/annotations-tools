from elasticsearch import Elasticsearch
import warnings
import argparse

warnings.filterwarnings("ignore")

index_name = "tmp2"
client = Elasticsearch(f"http://localhost:9200")

parser = argparse.ArgumentParser(description="Common hookpoints compatible to all functions in the call graph of the user-input function")
parser.add_argument("--func", required=True, help="Function name")

args = parser.parse_args()

def dfs(function_name):

    resp = client.search(index=index_name, pretty=True, source=["called_function_list", "compatibleHookpoints"], size=1000, query={
            "bool": {
                "must": {
                    "match_phrase": {
                    "funcName": function_name
                    }
                }
            }
        }).raw["hits"]["hits"][0]["_source"]

    content = resp["called_function_list"]
    compat = set(resp["compatibleHookpoints"])

    for func in content:
        compat = compat.intersection(dfs(func))
    
    return compat


hookpoints = dfs(args.func)
print(f"Compatible hookpoints throughout the FCG of function {args.func} : {hookpoints}")