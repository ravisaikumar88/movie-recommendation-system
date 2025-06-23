import React from "react";

function Sidebar({ onSelect }) {
  return (
    <div style={{
      width: "200px",
      background: "#282c34",
      color: "#fff",
      padding: "1rem",
      height: "100vh"
    }}>
      <h3>📊 Recommender</h3>
      <button onClick={() => onSelect("popular")} style={btnStyle}>Popular</button>
      <button onClick={() => onSelect("similar")} style={btnStyle}>Similar</button>
      <button onClick={() => onSelect("hybrid")} style={btnStyle}>Hybrid</button>
    </div>
  );
}

const btnStyle = {
  display: "block",
  margin: "1rem 0",
  padding: "0.5rem 1rem",
  background: "#61dafb",
  color: "#000",
  border: "none",
  cursor: "pointer",
};

export default Sidebar;
