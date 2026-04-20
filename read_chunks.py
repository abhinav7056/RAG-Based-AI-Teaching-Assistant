import requests
import os
import json
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import joblib


def create_embedding(text_list):

    r = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "bge-m3",
            "input": text_list
        }
    )

    response = r.json()

    
    if "embeddings" not in response:
        print("API Response Error:", response)
        return []

    return response["embeddings"]


jsons = os.listdir("jsons")

my_dicts = []
chunk_id = 0

for json_file in jsons:

    with open(f"jsons/{json_file}") as f:
        content = json.load(f)

    print(f"Creating Embeddings for {json_file}")

    embeddings = create_embedding([c['text'] for c in content['chunks']])


    if not embeddings:
        continue

    for i, chunk in enumerate(content['chunks']):
        chunk['chunk_id'] = chunk_id
        chunk['embedding'] = embeddings[i]

        chunk_id += 1
        my_dicts.append(chunk)

df = pd.DataFrame.from_records(my_dicts)
joblib.dump(df, 'embeddings.joblib')


