import { useState } from "react";
import api from "../api/axios";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post("/auth/login", { email, password });
      localStorage.setItem("token", res.data.access_token);
      window.location.href = "/analytics";
    } catch {
      setError("Invalid credentials");
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.overlay}></div>

      <div style={styles.card}>
        <h2 style={styles.title}>🍔 Food Delivery Login</h2>

        {error && <p style={styles.error}>{error}</p>}

        <form onSubmit={handleLogin}>
          <input
            style={styles.input}
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            style={styles.input}
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button style={styles.button}>Login</button>
        </form>
      </div>
    </div>
  );
}

const styles = {
  page: {
    height: "100vh",
    backgroundImage: `
      linear-gradient( 
        #ff6a00,
        #ee0979
      ),
      url("https://images.unsplash.com/photo-1600891964599-f61ba0e24092")
    `,
    backgroundSize: "cover",
    backgroundPosition: "center",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    position: "relative",
  },

  overlay: {
    position: "absolute",
    inset: 0,
    background:
      "url('https://images.unsplash.com/photo-1540189549336-e6e99c3679fe')",
    backgroundSize: "300px",
    opacity: 0.20, // 🔥 TRANSPARENCY
    pointerEvents: "none",
  },

  card: {
    background: "rgba(255,255,255,0.95)",
    padding: "40px",
    borderRadius: "16px",
    width: "350px",
    boxShadow: "0 20px 40px rgba(0,0,0,0.3)",
    zIndex: 1,
  },

  title: {
    textAlign: "center",
    marginBottom: "20px",
    color: "#ff6a00",
  },

  input: {
    width: "100%",
    padding: "12px",
    marginBottom: "15px",
    borderRadius: "8px",
    border: "1px solid #ccc",
  },

  button: {
    width: "100%",
    padding: "12px",
    background: "linear-gradient(135deg,#ff6a00,#ee0979)",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    fontSize: "16px",
    cursor: "pointer",
  },

  error: {
    color: "red",
    textAlign: "center",
    marginBottom: "10px",
  },
};
