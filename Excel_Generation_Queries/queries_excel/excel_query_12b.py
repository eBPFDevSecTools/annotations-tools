from elasticsearch import Elasticsearch
import argparse
from helpers import *
import pandas as pd
import os


def dfs(index_name, client, func, repo):
    resp = client.search(
        index=index_name,
        size=1000,
        pretty=True,
        fields=["called_function_list", "helper"],
        query={
            "bool": {
                "filter": {
                    "match_phrase": {
                        "File": repo
                    }
                },
                "must": {
                    "match_phrase": {
                        "funcName": func
                    }
                }
            }
        } 
    )

    response = resp["hits"]["hits"]

    helpers = []

    for d in response:
        if "fields" in d:
            if "helper" in d["fields"]:
                helpers = d["fields"]["helper"]
        
            if "called_function_list" in d["fields"]:
                for func_ in d["fields"]["called_function_list"]:
                    helpers += dfs(
                            index_name=index_name,
                            client=client,
                            func=func_,
                            repo=repo
                        )
    return helpers

def get_helpers_in_FCG(index_name, client):
    
    repos = get_all_repos(index_name=index_name, client=client)
    root_funcs = get_root_funcs(index_name=index_name, client=client)

    map_counts = pd.DataFrame(index=root_funcs, columns=repos + [f"{repo}_count" for repo in repos])

    num_helpers = {}

    for repo in repos:
        for func in root_funcs:

            HELPERS = dfs(
                index_name=index_name,
                client=client,
                func=func,
                repo=repo
            )
            
            HELPERS = set(HELPERS)

            map_counts.loc[func][repo] = list(HELPERS)
            map_counts.loc[func][f"{repo}_count"] = len(HELPERS)
            
        helpers_ = set()

        for helpers_list in map_counts[repo]:
            for f in num_helpers:
                helpers_.add(f)
        
        num_helpers[repo] = len(helpers_)

    if not os.path.isdir("../Query_CSVs"):
        os.makedirs("../Query_CSVs")
    
    map_counts.to_csv("../Query_CSVs/excel_query_12b_results.csv")

    return len(repos), num_helpers


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--index_name", required=True, help="Name of the Elasticsearch index")
    args = parser.parse_args()
    index_name = args.index_name

    client = Elasticsearch("http://localhost:9200")

    num_repos, num_helpers = get_helpers_in_FCG(index_name=index_name, client=client)

    print(f"Generated Excel for Query 12b - {num_repos} repos")
    print(num_helpers)