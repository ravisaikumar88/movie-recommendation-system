import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Load model and index
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("rag/index.faiss")

with open("rag/meta.pkl", "rb") as f:
    metadata = pickle.load(f)

def search_movies(query, top_k=3):
    # Convert query to embedding
    query_vec = model.encode([query])
    
    # Search in FAISS
    D, I = index.search(np.array(query_vec).astype("float32"), top_k)
    
    # Return results
    results = []
    for idx in I[0]:
        results.append(metadata[idx])
    return results


