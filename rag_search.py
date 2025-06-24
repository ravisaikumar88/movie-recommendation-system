# rag_search.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv("data/movies_metadata.csv", low_memory=False)
df = df[["title", "overview"]].dropna()

# Vectorize overviews
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["overview"])

# Search function
def search_movies(query, top_k=5):
    query_vec = vectorizer.transform([query])
    similarity_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = similarity_scores.argsort()[::-1][:top_k]
    results = df.iloc[top_indices][["title", "overview"]].to_dict(orient="records")
    return results
