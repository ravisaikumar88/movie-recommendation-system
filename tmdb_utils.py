import requests
from tmdb_config import api_key

def get_trending_movies_by_language(lang_code="en"):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&sort_by=popularity.desc&with_original_language={lang_code}"
    response = requests.get(url)
    data = response.json()
    
    if "results" not in data:
        return []
    
    return data["results"][:10]
