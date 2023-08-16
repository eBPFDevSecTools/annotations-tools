from elasticsearch import Elasticsearch
import warnings
import argparse

warnings.filterwarnings("ignore")

index_name = "tmp3"
client = Elasticsearch(f"http://localhost:9200")

parser = argparse.ArgumentParser(description="Generating the call graph of the user-input function in the user-input repository")
parser.add_argument("--repo", required=True, help="Name of the repository")
parser.add_argument("--func", required=True, help="Function Name")

args = parser.parse_args()

def dfs(function_name, call_graph_dict):
    call_graph_dict[function_name] = {}
    resp = client.search(index=index_name, pretty=True, source=["called_function_list"], size=1000, query={
            "bool": {
                "filter": {
                    "match_phrase": {
                    "File": args.repo
                    }
                },
                "must": {
                    "match_phrase": {
                    "funcName": function_name
                    }
                }
            }
        })
    # print(resp)
    content = resp.raw["hits"]["hits"][0]["_source"]["called_function_list"]
    # print(content)
    # content = resp.raw["hits"]["hits"]
    # print(len(content))

    for func in content:
        dfs(func, call_graph_dict=call_graph_dict[function_name])

call_graph = {}
dfs(args.func, call_graph_dict=call_graph)
print(f"Call graph for {args.func}")
print(call_graph)