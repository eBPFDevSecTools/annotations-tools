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
        fields=["called_function_list", "compatibleHookpoints"],
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

    compat = None

    for d in response:
        if "fields" in d:
            if "compatibleHookpoints" in d["fields"]:
                compat = set(d["fields"]["compatibleHookpoints"])
        
            if "called_function_list" in d["fields"]:
                for func_ in d["fields"]["called_function_list"]:
                    compat = compat.intersection(
                        dfs(
                            index_name=index_name,
                            client=client,
                            func=func_,
                            repo=repo
                        )
                    )
    return compat

def get_compatible_hookpoints(index_name, client):
    
    repos = get_all_repos(index_name=index_name, client=client)
    root_funcs = get_root_funcs(index_name=index_name, client=client)

    map_counts = pd.DataFrame(index=root_funcs, columns=repos + [f"{repo}_count" for repo in repos])
    
    num_hooks = {}

    for repo in repos:
        for func in root_funcs:

            compatibleHookpoints = dfs(
                index_name=index_name,
                client=client,
                func=func,
                repo=repo
            )


            if compatibleHookpoints is None:
                map_counts.loc[func][repo] = []
                map_counts.loc[func][f"{repo}_count"] = 0
            else:
                map_counts.loc[func][repo] = list(compatibleHookpoints)
                map_counts.loc[func][f"{repo}_count"] = len(compatibleHookpoints)
            
        hooks = set()

        for hook_list in map_counts[repo]:
            for f in hook_list:
                hooks.add(f)
        
        num_hooks[repo] = len(hooks)

    if not os.path.isdir("../Query_CSVs"):
        os.makedirs("../Query_CSVs")
    
    map_counts.to_csv("../Query_CSVs/excel_query_12a_results.csv")

    return len(repos), num_hooks


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--index_name", required=True, help="Name of the Elasticsearch index")
    args = parser.parse_args()
    index_name = args.index_name

    client = Elasticsearch("http://localhost:9200")

    num_repos, num_hooks = get_compatible_hookpoints(index_name=index_name, client=client)

    print(f"Generated Excel for Query 12a - {num_repos} repos")
    print(num_hooks)