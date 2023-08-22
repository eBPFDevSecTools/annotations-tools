from elasticsearch import Elasticsearch
import argparse
from helpers import *
import pandas as pd
import os

def get_number_of_maps(index_name, client):
    
    repos = get_all_repos(index_name=index_name, client=client)

    maps_counts = pd.DataFrame(index=repos, columns=["Maps", "Counts"])

    for repo in repos:
        maps = get_all_maps_from_repo(index_name=index_name, client=client, repo=repo)
        maps_counts.loc[repo]["Maps"] = maps
        maps_counts.loc[repo]["Counts"] = len(maps)

    if not os.path.isdir("../Query_CSVs"):
        os.makedirs("../Query_CSVs")
    
    maps_counts.to_csv("../Query_CSVs/excel_query_2_results.csv"                                                                                                                                                                                                                                                                                                                                                                    )

    return len(repos)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--index_name", required=True, help="Name of the Elasticsearch index")
    args = parser.parse_args()
    index_name = args.index_name

    client = Elasticsearch("http://localhost:9200")

    num_repos = get_number_of_maps(index_name=index_name, client=client)

    print(f"Generated Excel for Query 2 - {num_repos} repos")