from elasticsearch import Elasticsearch
import argparse
from helpers import *
import pandas as pd
import os

def get_number_of_functions(index_name, client):
    
    helper_funcs = get_all_helper_functions(index_name=index_name, client=client)
    repos = get_all_repos(index_name=index_name, client=client)

    funcs_nums = pd.DataFrame(columns=repos + [f"{repo}_count" for repo in repos], index=helper_funcs)


    number_funcs = {}

    for repo in repos:
        for helper_func in helper_funcs:
            
            # To Do: The requests need to be optimized
            resp = client.search(index=index_name, pretty=True, fields=["File", "funcName"], source=False, size=1000, query={
                "bool": {
                    "filter": {
                        "match_phrase": {
                            "File": repo 
                        }
                    },
                    "must": {
                        "match": {
                            "helper": helper_func
                        }
                    }  
                }
            })

            responses = resp.raw['hits']['hits']
        
            filenames = []

            for d in responses:
                if "fields" in d and "File" in d["fields"]:
                    filenames += d["fields"]["File"]
            
            funcs_nums.loc[helper_func][repo] = filenames
            funcs_nums.loc[helper_func][f"{repo}_count"] = len(filenames)
        
        funcs = set()
        for file_list in funcs_nums[repo]:
            for filename in file_list:
                funcs.add(filename)
        
        number_funcs[repo] = len(funcs)

    if not os.path.isdir("../Query_CSVs"):
        os.makedirs("../Query_CSVs")
    
    funcs_nums.to_csv("../Query_CSVs/excel_query_1_results.csv")

    return len(helper_funcs), number_funcs


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--index_name", required=True, help="Name of the Elasticsearch index")
    args = parser.parse_args()
    index_name = args.index_name

    client = Elasticsearch("http://localhost:9200")

    num_funcs, number_funcs = get_number_of_functions(index_name=index_name, client=client)

    print(f"Generated Excel for Query 1 - {num_funcs} helper functions")
    print(number_funcs)