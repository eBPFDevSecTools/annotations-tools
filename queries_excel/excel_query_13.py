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
        fields=["called_function_list"],
        query={
            "bool": {
                "must": {
                    "match_phrase": {
                        "funcName": func
                    }
                }
            }
        } 
    )

    response = resp["hits"]["hits"]

    size = 0

    for d in response:
        if "fields" in d and "called_function_list" in d["fields"]:
            for func_ in d["fields"]["called_function_list"]:
                size += dfs(
                        index_name=index_name,
                        client=client,
                        func=func_,
                        repo=repo
                    )
    return 1 + size

def get_average_FCG_size(index_name, client):
    
    repos = get_all_repos(index_name=index_name, client=client)

    avg_size_df = pd.DataFrame(index=repos, columns=["Average Size"])

    for repo in repos:
        root_funcs = get_root_funcs_from_repo(index_name=index_name, client=client, repo=repo)

        SIZE = 0

        for func in root_funcs:

            SIZE += dfs(
                index_name=index_name,
                client=client,
                func=func,
                repo=repo
            )
        
        SIZE /= len(root_funcs)

        avg_size_df.loc[repo]["Average Size"] = SIZE

    if not os.path.isdir("../Query_CSVs"):
        os.makedirs("../Query_CSVs")
    
    avg_size_df.to_csv("../Query_CSVs/excel_query_13_results.csv")

    return len(repos)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--index_name", required=True, help="Name of the Elasticsearch index")
    args = parser.parse_args()
    index_name = args.index_name

    client = Elasticsearch("http://localhost:9200")

    num_repos = get_average_FCG_size(index_name=index_name, client=client)

    print(f"Generated Excel for Query 13 - {num_repos} repos")