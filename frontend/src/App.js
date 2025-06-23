import React, { useState } from "react";
import "./App.css";

function App() {
  const [movies, setMovies] = useState([]);
  const [title, setTitle] = useState("Toy Story");
  const [mode, setMode] = useState("similar");

  const fetchRecommendations = async (type) => {
    let url = "http://127.0.0.1:8000/recommend";

    if (type === "popular") url += "/popular";
    else if (type === "similar") url += `/similar?title=${encodeURIComponent(title)}`;
    else if (type === "hybrid") url += `/hybrid?title=${encodeURIComponent(title)}&alpha=0.5`;

    setMode(type);

    try {
      const res = await fetch(url);
      const data = await res.json();
      setMovies(data);
    } catch (error) {
      console.error("Error fetching data:", error);
      setMovies([]);
    }
  };

  const getHeading = () => {
    switch (mode) {
      case "popular":
        return "🔥 Popular Movies";
      case "similar":
        return `🎯 Similar Movies for "${title}"`;
      case "hybrid":
        return `⚡ Hybrid Recommendations for "${title}"`;
      default:
        return "🎬 Recommendations";
    }
  };

  return (
    <div className="App">
      <div className="sidebar">
        <h2>🎥 Recommender</h2>
        <button onClick={() => fetchRecommendations("popular")}>Popular</button>
        <button onClick={() => fetchRecommendations("similar")}>Similar</button>
        <button onClick={() => fetchRecommendations("hybrid")}>Hybrid</button>
      </div>

      <div className="content">
        <h1>{getHeading()}</h1>

        {(mode === "similar" || mode === "hybrid") && (
          <div className="search-box">
            <input
              type="text"
              placeholder="Enter movie title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
            <button onClick={() => fetchRecommendations(mode)}>🔍 Search</button>
          </div>
        )}

        <ul className="movie-list">
          {movies.map((movie, index) => (
            <li key={index}>
              {typeof movie === "string" ? movie : movie.title || JSON.stringify(movie)}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
