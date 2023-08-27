from elasticsearch import Elasticsearch
import argparse
from helpers import *
import pandas as pd
import os

def get_number_of_functions(index_name, client):
    
    repos = get_all_repos(index_name=index_name, client=client)
    max_depth = max_call_depth(index_name=index_name, client=client)

    func_counts = pd.DataFrame(index=list(range(max_depth + 1)), columns=repos + [f"{repo}_count" for repo in repos])

    number_funcs = {}

    for repo in repos:
        for depth in range(max_depth + 1):
            resp = client.search(index=index_name, pretty=True, fields=["File", "funcName"], source=False, size=1000, query={
                "bool": {
                    "filter": {
                        "match_phrase": {
                            "File": repo 
                        }
                    },
                    "must": {
                        "match": {
                            "call_depth": depth
                        }
                    }  
                }
            })

            responses = resp.raw["hits"]["hits"]
            
            num_funcs = []
            for d in responses:
                if "fields" in d and "funcName" in d["fields"] and "File" in d["fields"]:
                    num_funcs.append(d["fields"]["funcName"][0] + " - " + d["fields"]['File'][0])
            # if repo == "ebpf-ratelimiter-main":
            #     print(num_funcs)
            func_counts.loc[depth][repo] = num_funcs
            func_counts.loc[depth][f"{repo}_count"] = len(num_funcs)
        
        funcs = set()
        funcs_tmp = []
        for func_list in func_counts[repo]:
            for f in func_list:
                funcs.add(f)
                funcs_tmp.append(f)
        
        # if repo == "ebpf-ratelimiter-main":
        #     MULTIDEFS = {}
        #     for f in list(funcs):
        #         MULTIDEFS[f] = funcs_tmp.count(f)
        #     print(repo)
        #     print(MULTIDEFS)

        # print(f"Repo - {repo}, Set_len = {len(funcs)}, List_len - {len(funcs_tmp)}")

        number_funcs[repo] = len(funcs)


    if not os.path.isdir("../Query_CSVs"):
        os.makedirs("../Query_CSVs")
    
    func_counts.to_csv("../Query_CSVs/excel_query_6_results.csv")

    return len(repos), number_funcs


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--index_name", required=True, help="Name of the Elasticsearch index")
    args = parser.parse_args()
    index_name = args.index_name

    client = Elasticsearch("http://localhost:9200")

    num_repos, funcs_set = get_number_of_functions(index_name=index_name, client=client)

    print(f"Generated Excel for Query 6 - {num_repos} repos")
    print(funcs_set)