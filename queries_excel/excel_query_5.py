from elasticsearch import Elasticsearch
import argparse
from helpers import *
import pandas as pd
import os

def dfs(index_name, client, func, repo, fcg):
    fcg[func] = {}
    resp = client.search(
        index=index_name,
        size=1000,
        fields=["called_function_list"],
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

    responses = resp["hits"]["hits"]

    for d in responses:
        if "fields" in d and "called_function_list" in d["fields"]:
            for f in d["fields"]["called_function_list"]:
                dfs(index_name, client, f, repo, fcg[func])

def get_FCGs(index_name, client):
    
    repos = get_all_repos(index_name=index_name, client=client)
    # print(repos)
    FCG = {}

    for repo in repos:
        root_funcs = get_root_funcs_from_repo(index_name=index_name, client=client, repo=repo)
        FCG[repo] = {}
        for func in root_funcs:
            call_graph = {}
            dfs(index_name, client, func, repo, call_graph)
            FCG[repo][func] = call_graph
    
    return FCG


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--index_name", required=True, help="Name of the Elasticsearch index")
    args = parser.parse_args()
    index_name = args.index_name

    client = Elasticsearch("http://localhost:9200")

    num_repos = get_FCGs(index_name=index_name, client=client)

    print(f"Generated Excel for Query 4 - {num_repos} repos")