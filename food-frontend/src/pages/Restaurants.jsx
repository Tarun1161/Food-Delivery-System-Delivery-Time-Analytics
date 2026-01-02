import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Restaurants() {
  const [restaurants, setRestaurants] = useState([]);

  useEffect(() => {
    api.get("/restaurants")
      .then((res) => setRestaurants(res.data))
      .catch(() => alert("Unauthorized or error"));
  }, []);

  return (
    <div>
      <h2>Restaurants</h2>
      <ul>
        {restaurants.map((r) => (
          <li key={r.id}>{r.name}</li>
        ))}
      </ul>
    </div>
  );
}
