import streamlit as st
import pandas as pd
from recommender import (
    get_top_movies,
    get_similar_movies,
    get_hybrid_recommendations,
    get_all_genres,
)
from rag_search import search_movies
from tmdb_utils import get_trending_movies_by_language

st.set_page_config(page_title="Movie Recommender", layout="centered")
st.title("🎬 Movie Recommender System")

# ---------------- Load movie titles ----------------
df_titles = pd.read_csv("data/movies_metadata.csv", low_memory=False)
movie_titles = df_titles["title"].dropna().unique().tolist()
movie_titles = sorted(list(set(movie_titles)))

# ---------------- Sidebar ----------------
st.sidebar.header("Choose Mode")
algo = st.sidebar.radio(
    "Recommendation Type:",
    ("Popularity", "Content-based (TF-IDF)", "Hybrid", "🧠 Ask a Movie Question (RAG)", "🔥 Trending")
)

# ---------------- Genre Filter (only for Popularity) ----------------
selected_genres = []
if algo == "Popularity":
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

# ---------------- CONTENT-BASED (TF-IDF) ----------------
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
        sim_list = get_similar_movies(movie, top_n=n)
        if not sim_list:
            st.warning("No similar movies found.")
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
    alpha = st.slider("Popularity vs Similarity  (α)", 0.0, 1.0, 0.5)

    if st.button("Get Hybrid Recommendations"):
        hybrid_list = get_hybrid_recommendations(movie, top_n=n, alpha=alpha)
        if not hybrid_list:
            st.warning("No recommendations found.")
        for m in hybrid_list:
            st.write("•", m)

# ---------------- RAG ----------------
elif algo == "🧠 Ask a Movie Question (RAG)":
    st.subheader("🧠 Smart Movie Q&A")
    question = st.text_input("Type your movie-related question:")
    if st.button("Ask"):
        if not question.strip():
            st.warning("Please enter a question before clicking Ask.")
        else:
            st.info("Using RAG to find matching movies...")
            results = search_movies(question)
            for res in results:
                st.markdown(f"**🎬 {res['title']}**")
                st.markdown(f"📝 {res['overview']}")
                st.markdown("---")

# ---------------- TRENDING ----------------
elif algo == "🔥 Trending":
    st.subheader("🔥 Trending Movies by Language")

    lang_map = {
        "English": "en",
        "Hindi": "hi",
        "Telugu": "te",
        "Tamil": "ta",
        "Malayalam": "ml"
    }

    selected_lang = st.sidebar.selectbox("Choose Language:", list(lang_map.keys()))
    lang_code = lang_map[selected_lang]

    trending = get_trending_movies_by_language(lang_code)

    if not trending:
        st.warning("No trending movies found.")
    else:
        for movie in trending:
            title = movie.get("title", "N/A")
            rating = movie.get("vote_average", "N/A")
            overview = movie.get("overview", "")
            poster_path = movie.get("poster_path", "")
            poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}" if poster_path else ""

            st.markdown(f"### 🎬 {title} — ⭐ {rating}")
            if poster_url:
                st.image(poster_url, width=150)
            if overview:
                st.write(overview)
            st.markdown("---")
