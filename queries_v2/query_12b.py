from elasticsearch import Elasticsearch
import warnings
import argparse

warnings.filterwarnings("ignore")

index_name = "tmp2"
client = Elasticsearch(f"http://localhost:9200")

class DataStruture:
    def __init__(self, funcName=None):
        self.funcName = funcName
        self.children = {}
        self.helper = None

parser = argparse.ArgumentParser(description="Helpers corresponding to the functions in the call graph of the user-input function")
parser.add_argument("--func", required=True, help="Function name")

args = parser.parse_args()

def dfs(function_name, datastructure):
    datastructure[function_name] = DataStruture(funcName=function_name)
    resp = client.search(index=index_name, pretty=True, source=["called_function_list", "helper"], size=1000, query={
            "bool": {
                "must": {
                    "match_phrase": {
                    "funcName": function_name
                    }
                }
            }
        }).raw["hits"]["hits"][0]["_source"]

    content = resp["called_function_list"]
    datastructure[function_name].helper = resp["helper"]

    for func in content:
        dfs(func, datastructure[function_name].children)

def printFCG(FCG):
    queue = []
    childFuncs = list(FCG.values())
    queue += childFuncs

    while(queue):
        child = queue.pop(0)
        print('Function Name : ', child.funcName)
        print('BPF Helper : ', child.helper)
        queue += list(child.children.values())


FCG = {}
dfs(args.func, datastructure=FCG)
print(f"FCG of function {args.func}")
printFCG(FCG)
    