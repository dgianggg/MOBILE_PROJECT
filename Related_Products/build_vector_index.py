import psycopg2
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Kết nối PostgreSQL
conn = psycopg2.connect(
    host="bytesme-singapore-cluster-1-test-aiven-minhduc-uit.k.aivencloud.com",
    port="17384",
    dbname="defaultdb",
    user="avnadmin",
    password="AVNS_cWnY-GoVwCtfwYowoRQ"
)

# Truy vấn sản phẩm
df = pd.read_sql_query("SELECT product_id, product_name, product_description FROM products", conn)
df['text'] = df['product_name'].fillna('') + '. ' + df['product_description'].fillna('')

# Tạo embedding
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(df['text'].tolist(), show_progress_bar=True)

# FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype('float32'))

# Lưu FAISS index + id mapping
faiss.write_index(index, "vector.index")
with open("id_mapping.pkl", "wb") as f:
    pickle.dump(dict(zip(range(len(df)), df['product_id'].tolist())), f)

# Tạo file related_products.json
related_dict = {}

for idx in range(len(df)):
    input_vec = np.array([embeddings[idx]]).astype('float32')
    D, I = index.search(input_vec, 6)
    related_ids = [
        int(df['product_id'][i]) for i in I[0]
        if int(df['product_id'][i]) != int(df['product_id'][idx])
    ]
    related_dict[str(int(df['product_id'][idx]))] = related_ids[:5]

# Ghi ra file JSON
import json
with open("related_products.json", "w", encoding="utf-8") as f:
    json.dump(related_dict, f, ensure_ascii=False, indent=2)

