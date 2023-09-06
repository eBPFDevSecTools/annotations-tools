from elasticsearch import Elasticsearch
import argparse
from helpers import *
import pandas as pd
import os


def dfs(index_name, client, func, repo, datastructure):
    resp = client.search(
        index=index_name,
        size=1000,
        pretty=True,
        fields=["called_function_list", "humanFuncDescription", "AI_func_description", "developer_inline_comments"],
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

    datastructure[func] = {}
    datastructure[func]["children"] = {}

    for d in response:
        if "fields" in d:
            if "humanFuncSescription" in d["fields"]:
                datastructure[func]["Human Description"] = d["fields"]["humanFuncDescription"]
            if "AI_func_description" in d["fields"]:
                datastructure[func]["AI Description"] = d["fields"]["AI_func_description"]
            if "developer_inline_comments" in d["fields"]:
                datastructure[func]["Developer_inline_comments"] = d["fields"]["developer_inline_comments"]
        
            if "called_function_list" in d["fields"]:
                for func_ in d["fields"]["called_function_list"]:
                    dfs(
                        index_name=index_name,
                        client=client,
                        func=func_,
                        repo=repo,
                        datastructure=datastructure[func]["children"]
                    )

def get_num_functions(datastructure):
    if not len(datastructure.keys()):
        return 0
    
    num_funcs = len(datastructure.keys())
    for k in datastructure.keys():
        num_funcs += get_num_functions(datastructure=datastructure[k]["children"])
    
    return num_funcs

def get_comments_in_FCG(index_name, client):
    
    repos = get_all_repos(index_name=index_name, client=client)
    root_funcs = get_root_funcs(index_name=index_name, client=client)

    funcs_counts = pd.DataFrame(index=root_funcs, columns=repos + [f"{repo}_count" for repo in repos])

    for repo in repos:
        for func in root_funcs:
            datastructure = {}
            dfs(
                index_name=index_name,
                client=client,
                func=func,
                repo=repo,
                datastructure=datastructure
            )

            funcs_counts.loc[func][repo] = datastructure
            funcs_counts.loc[func][f"{repo}_count"] = get_num_functions(datastructure)
            
    if not os.path.isdir("../Query_CSVs"):
        os.makedirs("../Query_CSVs")
    
    funcs_counts.to_csv("../Query_CSVs/excel_query_12c_results.csv")

    return len(repos)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--index_name", required=True, help="Name of the Elasticsearch index")
    args = parser.parse_args()
    index_name = args.index_name

    client = Elasticsearch("http://localhost:9200")

    num_repos = get_comments_in_FCG(index_name=index_name, client=client)

    print(f"Generated Excel for Query 12c - {num_repos} repos")