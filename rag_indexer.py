import pandas as pd
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer

def build_movie_index(data_path="data/movies_metadata.csv", index_path="rag/index.faiss", meta_path="rag/meta.pkl"):
    # Load and clean data
    df = pd.read_csv(data_path, low_memory=False)
    df = df[df["overview"].notnull()].reset_index(drop=True)
    
    # Load embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Get embeddings
    print("Generating embeddings...")
    embeddings = model.encode(df["overview"].tolist(), show_progress_bar=True)
    
    # Save metadata (title + overview)
    metadata = df[["title", "overview"]].to_dict(orient="records")
    with open(meta_path, "wb") as f:
        pickle.dump(metadata, f)

    # Build FAISS index
    print("Building FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))

    # Save index
    faiss.write_index(index, index_path)
    print("Index built and saved successfully!")

if __name__ == "__main__":
    build_movie_index()
