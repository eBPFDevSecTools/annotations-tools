from elasticsearch import Elasticsearch
import argparse
from helpers import *
import pandas as pd
import os

def get_number_of_functions(index_name, client):
    
    repos = get_all_repos(index_name=index_name, client=client)
    max_depth = max_call_depth(index_name=index_name, client=client)

    func_counts = pd.DataFrame(index=list(range(max_depth + 1)), columns=repos + [f"{repo}_count" for repo in repos])

    for repo in repos:
        for depth in range(max_depth + 1):
            resp = client.search(index=index_name, pretty=True, fields=["File", "funcName"], source=False, size=1000, query={
                "bool": {
                    "filter": {
                        "match_phrase": {
                            "File": repo 
                        }
                    },
                    "must": {
                        "match": {
                            "call_depth": depth
                        }
                    }  
                }
            })

            responses = resp.raw["hits"]["hits"]
            
            num_funcs = []
            for d in responses:
                if "fields" in d and "File" in d["fields"]:
                    num_funcs.append(d["fields"]['File'])
            
            func_counts.loc[depth][repo] = num_funcs
            func_counts.loc[depth][f"{repo}_count"] = len(num_funcs)


    if not os.path.isdir("../Query_CSVs"):
        os.makedirs("../Query_CSVs")
    
    func_counts.to_csv("../Query_CSVs/excel_query_6_results.csv")

    return len(repos)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--index_name", required=True, help="Name of the Elasticsearch index")
    args = parser.parse_args()
    index_name = args.index_name

    client = Elasticsearch("http://localhost:9200")

    num_repos = get_number_of_functions(index_name=index_name, client=client)

    print(f"Generated Excel for Query 6 - {num_repos} repos")