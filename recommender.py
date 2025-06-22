import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import requests

# ------------------------------------------------------------------
def load_data():
    df = pd.read_csv("data/movies_metadata.csv", low_memory=False)

    df = df[pd.to_numeric(df["vote_count"], errors="coerce").notnull()]
    df = df[pd.to_numeric(df["vote_average"], errors="coerce").notnull()]
    df["vote_count"] = df["vote_count"].astype(int)
    df["vote_average"] = df["vote_average"].astype(float)

    def parse_genre(val):
        try:
            items = ast.literal_eval(val)
            return [g["name"] for g in items]
        except Exception:
            return []

    df["genres_parsed"] = df["genres"].apply(parse_genre)
    return df


# ------------------------------------------------------------------
def get_all_genres():
    df = load_data()
    genres = set(g for sub in df["genres_parsed"] for g in sub)
    return sorted(genres)


# ------------------------------------------------------------------
def get_top_movies(n=10, min_votes=100, genres=None):
    df = load_data()
    df = df[df["vote_count"] >= min_votes]
    if genres:
        df = df[df["genres_parsed"].apply(lambda gs: any(g in gs for g in genres))]
    return df.sort_values("vote_average", ascending=False).head(n)[
        ["title", "vote_average", "vote_count"]
    ]


# ------------------------------------------------------------------
def get_similar_movies(title, top_n=10, genres=None):
    df = load_data()
    df = df[df["overview"].notnull()].reset_index(drop=True)

    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df["overview"])

    indices = pd.Series(df.index, index=df["title"]).drop_duplicates()
    idx = indices.get(title)

    if idx is None:
        return ["❌ Movie not found in dataset."]

    cosine_sim = linear_kernel(tfidf_matrix[idx], tfidf_matrix).flatten()
    sim_indices = cosine_sim.argsort()[-top_n - 1 : -1][::-1]
    recs = df["title"].iloc[sim_indices].tolist()

    if genres:
        recs = [
            t
            for t in recs
            if any(g in df.loc[df["title"] == t, "genres_parsed"].iloc[0] for g in genres)
        ]

    return recs[:top_n]


# ------------------------------------------------------------------
def get_hybrid_recommendations(title, top_n=10, genres=None, alpha=0.5):
    df = load_data()
    df = df[df["overview"].notnull()].reset_index(drop=True)

    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df["overview"])

    indices = pd.Series(df.index, index=df["title"]).drop_duplicates()
    idx = indices.get(title)
    if idx is None:
        return ["❌ Movie not found in dataset."]

    cosine_sim = linear_kernel(tfidf_matrix[idx], tfidf_matrix).flatten()
    df["norm_vote"] = (df["vote_average"] - df["vote_average"].min()) / (
        df["vote_average"].max() - df["vote_average"].min()
    )
    df["hybrid_score"] = alpha * cosine_sim + (1 - alpha) * df["norm_vote"]

    if genres:
        df = df[df["genres_parsed"].apply(lambda g: any(x in g for x in genres))]

    top = df.sort_values("hybrid_score", ascending=False).head(top_n)
    return top["title"].tolist()
