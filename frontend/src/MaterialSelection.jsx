
import { useEffect, useState } from "react";

function MaterialSelection() {
  const [materials, setMaterials] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadMaterials() {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/materials"
        );

        if (!response.ok) {
          throw new Error("Failed to load materials");
        }

        const data = await response.json();

        setMaterials(data.materials);

      } catch (err) {
        console.error("Material API Error:", err);
        setError("Unable to load material information");
      } finally {
        setLoading(false);
      }
    }

    loadMaterials();
  }, []);

  if (loading) {
    return <p>Loading engineering materials...</p>;
  }

  if (error) {
    return <p style={{ color: "red" }}>{error}</p>;
  }

  return (
    <section className="orders-section">

      <h2>Engineering Material Selection</h2>

      <p>
        Compare materials available for roll forming.
      </p>

      <table className="orders-table">

        <thead>
          <tr>
            <th>Material Code</th>
            <th>Material Name</th>
            <th>Grade</th>
            <th>Density (kg/m³)</th>
            <th>Price / kg (sample units)</th>
          </tr>
        </thead>

        <tbody>
          {Object.entries(materials).map(
            ([code, material]) => (
              <tr key={code}>
                <td>{code}</td>
                <td>{material.name}</td>
                <td>{material.grade}</td>
                <td>{material.density.toLocaleString()}</td>
                <td>{material.price_per_kg.toFixed(2)}</td>
              </tr>
            )
          )}
        </tbody>

      </table>

    </section>
  );
}

export default MaterialSelection;
