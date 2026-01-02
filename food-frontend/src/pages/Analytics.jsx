import { useEffect, useState } from "react";
import api from "../api/axios";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";

/* 🎨 COLORS FOR PIE */
const COLORS = ["#ff6a00", "#6a11cb", "#00c6ff", "#00c853", "#ff1744"];

export default function Analytics() {
  const [avgTime, setAvgTime] = useState(0);
  const [dailyPeak, setDailyPeak] = useState([]);
  const [topRestaurants, setTopRestaurants] = useState([]);

  useEffect(() => {
    api.get("/analytics/avg-delivery-time")
      .then(res => setAvgTime(res.data.average_delivery_time_minutes));

    api.get("/analytics/peak-hour/daily")
      .then(res => setDailyPeak(res.data));

    api.get("/analytics/top-restaurants")
      .then(res => setTopRestaurants(res.data));
  }, []);

  return (
    <div style={styles.page}>
      <h1 style={styles.heading}>📊 Analytics Dashboard</h1>

      {/* Avg Delivery Card */}
      <div style={styles.cardRow}>
        <div style={styles.card}>
          <h3>⏱ Average Delivery Time</h3>
          <p style={styles.bigNumber}>{avgTime} min</p>
        </div>
      </div>

      {/* Daily Peak Hour */}
      <div style={styles.section}>
        <h2>🔥 Daily Peak Hours</h2>

        {dailyPeak.length === 0 ? (
          <p>No peak-hour data available</p>
        ) : (
          <div style={{ width: "100%", height: 300 }}>
            <ResponsiveContainer>
              <BarChart data={dailyPeak}>
                <XAxis dataKey="hour" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="orders" fill="#ff6a00" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Top Restaurants Pie Chart */}
      <div style={styles.section}>
        <h2>🏆 Top Restaurants</h2>

        {topRestaurants.length === 0 ? (
          <p>No restaurant data available</p>
        ) : (
          <div style={{ width: "100%", height: 350 }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie
                  data={topRestaurants}
                  dataKey="orders"
                  nameKey="restaurant"
                  cx="50%"
                  cy="50%"
                  outerRadius={120}
                  label
                >
                  {topRestaurants.map((_, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>

                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  );
}

/* 🎨 STYLES (OUTSIDE COMPONENT) */
const styles = {
  page: {
    minHeight: "100vh",
    padding: "30px",
    background: "linear-gradient(135deg, #667eea, #764ba2)",
    color: "#fff",
  },
  heading: {
    textAlign: "center",
    marginBottom: "40px",
    fontSize: "32px",
  },
  cardRow: {
    display: "flex",
    justifyContent: "center",
    marginBottom: "40px",
  },
  card: {
    background: "#ffffff",
    color: "#333",
    padding: "25px",
    borderRadius: "15px",
    width: "280px",
    textAlign: "center",
    boxShadow: "0 15px 30px rgba(0,0,0,0.25)",
  },
  bigNumber: {
    fontSize: "36px",
    fontWeight: "bold",
    color: "#ff6a00",
  },
  section: {
    background: "#ffffff",
    color: "#333",
    padding: "25px",
    borderRadius: "15px",
    marginBottom: "40px",
    boxShadow: "0 15px 30px rgba(0,0,0,0.25)",
  },
};

