import streamlit as st
import pandas as pd
from recommender import (
    get_top_movies,
    get_similar_movies,
    get_hybrid_recommendations,
    get_all_genres,
)

st.set_page_config(page_title="Movie Recommender", layout="centered")
st.title("🎬 Movie Recommender System")

# ---------------- Load movie titles for autocomplete ----------------
df_titles = pd.read_csv("data/movies_metadata.csv", low_memory=False)
movie_titles = df_titles["title"].dropna().unique().tolist()
movie_titles = sorted(list(set(movie_titles)))

# ---------------- Sidebar ----------------
st.sidebar.header("Algorithm")
algo = st.sidebar.radio(
    "Choose recommendation method:",
    ("Popularity", "Content-based (TF-IDF)", "Hybrid"),
)

# ---------------- Genre Filter ----------------
st.sidebar.header("Filters")
all_genres = get_all_genres()
selected_genres = st.sidebar.multiselect("Select genres (optional):", all_genres)

# ---------------- POPULARITY ----------------
if algo == "Popularity":
    st.subheader("🔝 Top-Rated Movies")
    n = st.slider("How many movies?", 5, 20, 10)
    if st.button("Recommend"):
        results = get_top_movies(n=n, genres=selected_genres)
        for _, row in results.iterrows():
            st.write(
                f"**{row['title']}** — ⭐ {row['vote_average']} "
                f"({row['vote_count']} votes)"
            )

# ---------------- CONTENT-BASED ----------------
elif algo == "Content-based (TF-IDF)":
    st.subheader("🔍 Find Similar Movies")
    movie = st.selectbox(
        "Choose a movie title:",
        movie_titles,
        index=movie_titles.index("Toy Story") if "Toy Story" in movie_titles else 0,
        key="tfidf_box"
    )
    n = st.slider("How many similar movies?", 5, 20, 10, key="tfidf_slider")
    if st.button("Find Similar"):
        sim_list = get_similar_movies(movie, top_n=n, genres=selected_genres)
        if not sim_list:
            st.warning("No similar movies found for selected genres.")
        for m in sim_list:
            st.write("•", m)

# ---------------- HYBRID ----------------
elif algo == "Hybrid":
    st.subheader("🎯 Hybrid Recommendations")
    movie = st.selectbox(
        "Choose a movie title:",
        movie_titles,
        index=movie_titles.index("Toy Story") if "Toy Story" in movie_titles else 0,
        key="hybrid_box"
    )
    n = st.slider("How many results?", 5, 20, 10, key="hybrid_slider")
    alpha = st.slider("Similarity vs Popularity (α)", 0.0, 1.0, 0.5)

    if st.button("Get Hybrid Recommendations"):
        hybrid_list = get_hybrid_recommendations(movie, top_n=n, genres=selected_genres, alpha=alpha)
        if not hybrid_list:
            st.warning("No recommendations found for selected genres.")
        for m in hybrid_list:
            st.write("•", m)
