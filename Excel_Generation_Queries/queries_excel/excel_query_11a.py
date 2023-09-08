from elasticsearch import Elasticsearch
import argparse
from helpers import *
import pandas as pd
import os

def dfs(index_name, client, func, repo, prod_cons_pairs, updateMaps, prev=None):
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
            # print(func, d["fields"])
            if "readMaps" in d["fields"]:
                readMaps = d["fields"]["readMaps"]

                if set(updateMaps).intersection(set(readMaps)):
                    prod_cons_pairs.append({"parent": prev, "successor": func})
            
            if "updateMaps" in d["fields"]:
                updateMaps = d["fields"]["updateMaps"]
            
            if "called_function_list" in d["fields"]:
                for func_ in d["fields"]["called_function_list"]:
                    dfs(
                        index_name=index_name,
                        client=client,
                        func=func_,
                        repo=repo,
                        prod_cons_pairs=prod_cons_pairs,
                        updateMaps=updateMaps,
                        prev=func
                    )

def get_number_of_producer_consumer_pairs(index_name, client):
    
    repos = get_all_repos(index_name=index_name, client=client)
    root_funcs = get_root_funcs(index_name=index_name, client=client)

    pair_counts = pd.DataFrame(index=root_funcs, columns=repos + [f"{repo}_count" for repo in repos])

    for repo in repos:
        for func in root_funcs:
            
            prod_cons_pairs = []
            updateMaps = []

            dfs(
                index_name=index_name,
                client=client,
                func=func,
                repo=repo,
                prod_cons_pairs=prod_cons_pairs,
                updateMaps=updateMaps,
                prev=None
            )



            pair_counts.loc[func][repo] = list(prod_cons_pairs)
            pair_counts.loc[func][f"{repo}_count"] = len(prod_cons_pairs)
            

    if not os.path.isdir("../Query_CSVs"):
        os.makedirs("../Query_CSVs")
    
    pair_counts.to_csv("../Query_CSVs/excel_query_11a_results.csv")

    return len(repos)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--index_name", required=True, help="Name of the Elasticsearch index")
    args = parser.parse_args()
    index_name = args.index_name

    client = Elasticsearch("http://localhost:9200")

    num_repos = get_number_of_producer_consumer_pairs(index_name=index_name, client=client)

    print(f"Generated Excel for Query 11a - {num_repos} repos")