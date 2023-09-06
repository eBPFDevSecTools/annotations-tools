import numpy as np
import json

def similarity_scores(vector1, vector2, type="cosine"):
    if type == "cosine":
        return np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
    if type == "knn":
        return np.linalg.norm(vector1 - vector2)

def pairwise_similarity_scores(data, type="cosine", k=20):
    function_pairs = []
    num_functions = len(data.keys())

    for key1 in range(num_functions):
        for key2 in range(key1 + 1, num_functions):
            print(key1, key2)
            dic = {
                    "func1": {"Name": data[str(key1)]["funcName"], "File": data[str(key1)]["File"], "Key": key1},
                    "func2": {"Name": data[str(key2)]["funcName"], "File": data[str(key2)]["File"], "Key": key2}
            }
            sim_score = similarity_scores(data[str(key1)]["human_dense_vectors"][0], data[str(key2)]["human_dense_vectors"][0], type=type)
            dic["similarity"] = sim_score
            function_pairs.append(dic)

    sorted_func_pairs = sorted(function_pairs, key=lambda x: x["similarity"], reverse=True)
    return sorted_func_pairs[:k]

def pairwise_similarity_scores_llama(data, type="cosine", k=20):
    function_pairs = []
    num_functions = len(data)

    for key1 in range(num_functions):
        for key2 in range(key1 + 1, num_functions):
            if "llama_embeddings" not in data[key1] or "llama_embeddings" not in data[key2]:
                continue

            print(key1, key2)
            dic = {
                    "func1": {"Name": data[key1]["Function"], "File": data[key1]["File"], "Key": key1},
                    "func2": {"Name": data[key2]["Function"], "File": data[key2]["File"], "Key": key2}
            }
            sim_score = similarity_scores(data[key1]["llama_embeddings"][0], data[key2]["llama_embeddings"][0], type=type)
            dic["similarity"] = sim_score
            function_pairs.append(dic)

    sorted_func_pairs = sorted(function_pairs, key=lambda x: x["similarity"], reverse=True)
    return sorted_func_pairs[:k]

if __name__ == '__main__':
    data = json.load(open("human_annotations_dense_vecs.json", "r"))
    top_k = 50
    func_pairs = pairwise_similarity_scores(data, k=top_k)

    json.dump(func_pairs, open("human_annotations_sim_scores.json", "w"))

    data2 = json.load(open("data.json", "r"))
    func_pairs_2 = pairwise_similarity_scores_llama(data2, k=top_k)

    json.dump(func_pairs_2, open("llama_sim_scores.json", "w"))
