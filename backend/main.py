from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import recommender

app = FastAPI()

# Allow frontend (React) to connect later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Movie Recommender API is alive!"}

@app.get("/recommend/popular")
def recommend_popular(count: int = 10, genres: Optional[List[str]] = Query(None)):
    result = recommender.get_top_movies(n=count, genres=genres)
    return result.to_dict(orient="records")

@app.get("/recommend/similar")
def recommend_similar(title: str, count: int = 10, genres: Optional[List[str]] = Query(None)):
    result = recommender.get_similar_movies(title, top_n=count, genres=genres)
    return result

@app.get("/recommend/hybrid")
def recommend_hybrid(title: str, count: int = 10, alpha: float = 0.5, genres: Optional[List[str]] = Query(None)):
    result = recommender.get_hybrid_recommendations(title, top_n=count, genres=genres, alpha=alpha)
    return result
