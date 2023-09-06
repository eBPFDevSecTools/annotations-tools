from elasticsearch import Elasticsearch
import argparse
from helpers import *
import pandas as pd
import os

def dfs(index_name, client, func, repo, readMaps, updateMaps):
    resp = client.search(
        index=index_name,
        size=1000,
        pretty=True,
        fields=["called_function_list", "readMaps", "updateMaps"],
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

    for d in response:
        if "fields" in d:
            if "readMaps" in d["fields"]:
                readMaps += d["fields"]["readMaps"]
            if "updateMaps" in d["fields"]:
                updateMaps += d["fields"]["updateMaps"]
        
            if "called_function_list" in d["fields"]:
                for func_ in d["fields"]["called_function_list"]:
                    dfs(
                        index_name=index_name,
                        client=client,
                        func=func_,
                        repo=repo,
                        readMaps=readMaps,
                        updateMaps=updateMaps
                    )

def get_number_of_functions(index_name, client):
    
    repos = get_all_repos(index_name=index_name, client=client)
    root_funcs = get_root_funcs(index_name=index_name, client=client)

    map_counts = pd.DataFrame(index=root_funcs, columns=repos + [f"{repo}_count" for repo in repos])

    num_maps = {}

    for repo in repos:
        for func in root_funcs:
            
            readMaps = []
            updateMaps = []
            dfs(
                index_name=index_name,
                client=client,
                func=func,
                repo=repo,
                readMaps=readMaps,
                updateMaps=updateMaps
            )

            readMaps = set(readMaps)
            updateMaps = set(updateMaps)
            READUPDATE_MAPS = updateMaps.intersection(readMaps)

            map_counts.loc[func][repo] = list(READUPDATE_MAPS)
            map_counts.loc[func][f"{repo}_count"] = len(READUPDATE_MAPS)
        
        maps_ = set()

        for map_list in map_counts[repo]:
            for f in map_list:
                maps_.add(f)
        
        num_maps[repo] = len(maps_)          

    if not os.path.isdir("../Query_CSVs"):
        os.makedirs("../Query_CSVs")
    
    map_counts.to_csv("../Query_CSVs/excel_query_10_results.csv")

    return len(repos), num_maps


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--index_name", required=True, help="Name of the Elasticsearch index")
    args = parser.parse_args()
    index_name = args.index_name

    client = Elasticsearch("http://localhost:9200")

    num_repos, num_maps = get_number_of_functions(index_name=index_name, client=client)

    print(f"Generated Excel for Query 10 - {num_repos} repos")
    print(num_maps)