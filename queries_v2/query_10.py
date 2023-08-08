from elasticsearch import Elasticsearch
import warnings
import argparse
warnings.filterwarnings("ignore")

index_name = "tmp3"
client = Elasticsearch(f"http://localhost:9200")

parser = argparse.ArgumentParser(description="Maps which are being used by the functions in the call graph of user-input function")
parser.add_argument("--func", required=True, help="Function name")

args = parser.parse_args()

def dfs(function_name, readMaps_list, updateMaps_list):

    resp = client.search(index=index_name, pretty=True, source=["called_function_list", "updateMaps", "readMaps"], size=1000, query={
            "bool": {
                "must": {
                    "match_phrase": {
                    "funcName": function_name
                    }
                }
            }
        }).raw["hits"]["hits"][0]["_source"]

    content = resp["called_function_list"]
    updateMaps_list += resp['updateMaps']
    readMaps_list += resp['readMaps']
    for func in content:
        dfs(func, readMaps_list, updateMaps_list)

READ_MAPS = []
WRITE_MAPS = []
dfs(args.func, READ_MAPS, WRITE_MAPS)
print(f"Maps used throughout the FCG of function {args.func}")
print("Read Maps : ", READ_MAPS)
print("Written Maps : ", WRITE_MAPS)