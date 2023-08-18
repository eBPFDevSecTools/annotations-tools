from elasticsearch import Elasticsearch
import warnings

warnings.filterwarnings("ignore")


def get_all_helper_functions(index_name, client):
    resp = client.search(
        index=index_name,
        source=False,
        fields=["helper"],
        size=1000,
        query={"match_all": {}},
    )

    responses = resp["hits"]["hits"]

    helpers = set()

    for d in responses:
        if "fields" in d and "helper" in d["fields"]:
            for helper in d["fields"]["helper"]:
                helpers.add(helper)

    return list(helpers)

def get_all_maps_from_repo(index_name, client, repo):
    resp = client.search(
        index=index_name,
        source=False,
        fields=["readMaps", "updateMaps"],
        size=1000,
        query={"match": {"File": repo}},
    )

    responses = resp["hits"]["hits"]

    maps = set()

    for d in responses:
        if "fields" in d:
            if "readMaps" in d["fields"]:
                for map in d["fields"]["readMaps"]:
                    maps.add(map)
            
            if "updateMaps" in d["fields"]:
                for map in d["fields"]["updateMaps"]:
                    maps.add(map)

    return list(maps)

def get_all_maps(index_name, client):
    resp = client.search(
        index=index_name,
        source=False,
        fields=["readMaps", "updateMaps"],
        size=1000,
        query={"match_all": {}},
    )

    responses = resp["hits"]["hits"]

    maps = set()

    for d in responses:
        if "fields" in d:
            if "readMaps" in d["fields"]:
                for map in d["fields"]["readMaps"]:
                    maps.add(map)
            
            if "updateMaps" in d["fields"]:
                for map in d["fields"]["updateMaps"]:
                    maps.add(map)

    return list(maps)

def get_root_funcs(index_name, client):
    resp = client.search(
        index=index_name,
        source=False,
        fields=["funcName", "is_root_fn"],
        size=1000,
        query={"match_all": {}}
    )

    responses = resp["hits"]['hits']

    root_funcs = set() 

    for d in responses:
        if "fields" in d and "is_root_fn" in d["fields"]:
            if d["fields"]["is_root_fn"][0] == 1 and "funcName" in d["fields"]:
                root_funcs.add(d["fields"]["funcName"][0])
    
    return list(root_funcs)


def get_root_funcs_from_repo(index_name, client, repo):
    resp = client.search(
        index=index_name,
        source=False,
        fields=["funcName", "is_root_fn"],
        size=1000,
        query={"match": {"File": repo}}
    )

    responses = resp["hits"]["hits"]

    root_funcs = set()

    for d in responses:
        if "fields" in d and "is_root_fn" in d["fields"]:
            if d["fields"]["is_root_fn"][0] == 1 and "funcName" in d["fields"]:
                root_funcs.add(d["fields"]["funcName"][0])
    
    return list(root_funcs)


def max_call_depth(index_name, client):
    resp = client.search(
        index=index_name,
        source=False,
        fields=["call_depth"],
        size=1000,
        query={"match_all": {}}
    )

    responses = resp["hits"]["hits"]

    max_depth = 0

    for d in responses:
        if "fields" in d and "call_depth" in d["fields"]:
            max_depth = max(max_depth, d["fields"]["call_depth"][0])

    return max_depth

def get_all_repos(index_name, client):
    resp = client.search(
        index=index_name,
        source=False,
        fields=["File"],
        size=1000,
        query={"match_all": {}}
    )

    responses = resp["hits"]["hits"]

    repositories = set()

    for d in responses:
        if "fields" in d and "File" in d["fields"]:
            filename = d["fields"]["File"][0]
            dirs = filename.split("/")
            # print(dirs)
            if "examples" in dirs:
                repo_name = dirs[dirs.index("examples") + 1]
            elif "projects" in dirs:
                repo_name = dirs[dirs.index("projects") + 1]
            repositories.add(repo_name)
    
    return list(repositories)


if __name__ == "__main__":
    index_name = "tmp3"
    client = Elasticsearch("http://localhost:9200")

    helpers = get_all_helper_functions(index_name=index_name, client=client)
    print(len(helpers))

    maps = get_all_maps(index_name=index_name, client=client)
    print(len(maps))

    root_funcs = get_root_funcs(index_name=index_name, client=client)
    print(len(root_funcs))

    max_call_depth = max_call_depth(index_name=index_name, client=client)
    print(max_call_depth)

    repos = get_all_repos(index_name=index_name, client=client)
    print(repos)