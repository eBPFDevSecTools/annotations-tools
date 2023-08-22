from elasticsearch import Elasticsearch
import argparse
from helpers import *
import pandas as pd
import os

def get_number_of_maps(index_name, client):
    
    repos = get_all_repos(index_name=index_name, client=client)
    maps = get_all_maps(index_name=index_name, client=client)

    func_counts = pd.DataFrame(index=maps, columns=repos + [f"{repo}_count" for repo in repos])

    for repo in repos:
        for map in maps:
            resp = client.search(index=index_name, pretty=True, fields=["File", "funcName"], source=False, size=1000, query={
                "bool": {
                    "filter": {
                        "match_phrase": {
                            "File": repo 
                        }
                    },
                    "must": {
                        "match": {
                            "readMaps": map
                        }
                    }  
                }
            })

            responses = resp.raw["hits"]["hits"]
            
            num_funcs = []
            for d in responses:
                if "fields" in d and "File" in d["fields"]:
                    num_funcs.append(d["fields"]["File"])
            
            func_counts.loc[map][repo] = num_funcs
            func_counts.loc[map][f"{repo}_count"] = len(num_funcs)


    if not os.path.isdir("../Query_CSVs"):
        os.makedirs("../Query_CSVs")
    
    func_counts.to_csv("../Query_CSVs/excel_query_3_results.csv")

    return len(repos)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--index_name", required=True, help="Name of the Elasticsearch index")
    args = parser.parse_args()
    index_name = args.index_name

    client = Elasticsearch("http://localhost:9200")

    num_repos = get_number_of_maps(index_name=index_name, client=client)

    print(f"Generated Excel for Query 3 - {num_repos} repos")