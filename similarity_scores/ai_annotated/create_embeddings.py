import json
import os
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel

class Encoder:
    def __init__(self, model_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def encode(self, text: str, max_length: int):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=max_length)

        with torch.no_grad():
            model_output = self.model(**inputs, return_dict=True)

        # Perform pooling
        embeddings = self.mean_pooling(model_output, inputs['attention_mask'])
        # Normalize embeddings
        embeddings = F.normalize(embeddings, p=2, dim=1)
        return embeddings.detach().cpu().numpy()

    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)



def get_embeddings(encoder, datapath):
    data = json.load(open(datapath, "r"))

    for i, d in enumerate(data):
        print(i, d["Function"])
        if "LLaMa comments" not in d:
            continue

        if isinstance(d["LLaMa comments"], int):
            continue

        d["llama_embeddings"] = encoder.encode(d["LLaMa comments"].strip(), 512).tolist()

    json.dump(data, open(datapath, "w"))


if __name__ == '__main__':
    encoder = Encoder('sentence-transformers/msmarco-MiniLM-L6-cos-v5')
    datapath = "data.json"
    get_embeddings(encoder, datapath)


