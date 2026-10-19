
import { useState } from "react";

function MaterialRecommendation() {
  // Material requirements
  const [maxPrice, setMaxPrice] = useState("");
  const [maxDensity, setMaxDensity] = useState("");
  const [minYieldStrength, setMinYieldStrength] = useState("");

  // Machine requirements
  const [machineCode, setMachineCode] = useState("");
  const [thickness, setThickness] = useState("");
  const [stripWidth, setStripWidth] = useState("");

  // Recommendation results
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  // Send requirements to FastAPI
  async function handleRecommend(event) {
    event.preventDefault();

    setLoading(true);
    setMessage("");
    setRecommendations([]);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/recommend-materials",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            max_price: Number(maxPrice),
            max_density: Number(maxDensity),
            machine_code: machineCode || null,
            thickness_mm: machineCode
              ? Number(thickness)
              : null,
            strip_width_mm: machineCode
              ? Number(stripWidth)
              : null,
            min_yield_strength_mpa:
              minYieldStrength.trim() === ""
                ? null
                : Number(minYieldStrength),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : "Unable to get recommendations"
        );
      }

      setRecommendations(data.recommendations);

      if (data.total_matches === 0) {
        setMessage(
          "No materials match your requirements. " +
          "Check your price, density, machine limits, " +
          "and minimum yield strength. Materials without " +
          "documented minimum strengths are excluded " +
          "when a strength requirement is entered."
        );
      }
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  function displayStrength(value) {
    return typeof value === "number"
      ? `${value} MPa`
      : "Not established";
  }

  function displayStrengthType(type) {
    if (type === "published_minimum") {
      return "Published minimum";
    }

    if (type === "typical") {
      return "Typical reference";
    }

    if (type === "not_guaranteed") {
      return "Not guaranteed";
    }

    return "Not specified";
  }

  return (
    <section className="recommendation-section">
      <h2>Intelligent Material Recommendation</h2>

      <p>
        Enter material, machine, and optional strength
        requirements to find matching materials.
      </p>

      <form
        className="recommendation-form"
        onSubmit={handleRecommend}
      >
        {/* MAXIMUM MATERIAL PRICE */}
        <div>
          <label htmlFor="max-price">
            Maximum Price per kg
          </label>

          <input
            id="max-price"
            type="number"
            step="0.01"
            min="0.01"
            value={maxPrice}
            onChange={(e) => setMaxPrice(e.target.value)}
            placeholder="Example: 5.00"
            required
          />
        </div>

        {/* MAXIMUM MATERIAL DENSITY */}
        <div>
          <label htmlFor="max-density">
            Maximum Density (kg/m³)
          </label>

          <input
            id="max-density"
            type="number"
            step="any"
            min="0.01"
            value={maxDensity}
            onChange={(e) => setMaxDensity(e.target.value)}
            placeholder="Example: 8500"
            required
          />
        </div>

        {/* MINIMUM YIELD STRENGTH */}
        <div>
          <label htmlFor="min-yield-strength">
            Minimum Yield Strength (MPa) — Optional
          </label>

          <input
            id="min-yield-strength"
            type="number"
            step="any"
            min="0.01"
            value={minYieldStrength}
            onChange={(e) =>
              setMinYieldStrength(e.target.value)
            }
            placeholder="Example: 200"
          />

          <small>
            When specified, only materials with a
            documented minimum yield strength meeting
            this requirement are returned.
          </small>
        </div>

        {/* MACHINE SELECTION */}
        <div>
          <label htmlFor="machine-code">
            Select Machine
          </label>

          <select
            id="machine-code"
            value={machineCode}
            onChange={(e) => {
              setMachineCode(e.target.value);
              setThickness("");
              setStripWidth("");
            }}
          >
            <option value="">
              No machine selected
            </option>

            <option value="RF100">
              SmartRoll Demo RF100
            </option>

            <option value="RF200">
              SmartRoll Demo RF200
            </option>
          </select>
        </div>

        {/* MACHINE DIMENSION REQUIREMENTS */}
        {machineCode && (
          <>
            <div>
              <label htmlFor="material-thickness">
                Material Thickness (mm)
              </label>

              <input
                id="material-thickness"
                type="number"
                step="any"
                min="0.01"
                value={thickness}
                onChange={(e) =>
                  setThickness(e.target.value)
                }
                placeholder="Example: 1.5"
                required
              />
            </div>

            <div>
              <label htmlFor="strip-width">
                Strip Width (mm)
              </label>

              <input
                id="strip-width"
                type="number"
                step="any"
                min="0.01"
                value={stripWidth}
                onChange={(e) =>
                  setStripWidth(e.target.value)
                }
                placeholder="Example: 400"
                required
              />
            </div>
          </>
        )}

        {/* SUBMIT BUTTON */}
        <button type="submit" disabled={loading}>
          {loading
            ? "Finding Materials..."
            : "Recommend Materials"}
        </button>
      </form>

      {/* SUCCESS / ERROR MESSAGE */}
      {message && (
        <p role="status">{message}</p>
      )}

      {/* RECOMMENDATION RESULTS */}
      {recommendations.length > 0 && (
        <div>
          <h3>
            Recommended Materials ({recommendations.length})
          </h3>

          <div style={{ overflowX: "auto" }}>
            <table>
              <thead>
                <tr>
                  <th>Material</th>
                  <th>Grade</th>
                  <th>Density (kg/m³)</th>
                  <th>Price/kg</th>
                  <th>Minimum Yield Strength</th>
                  <th>Tensile Strength</th>
                  <th>Strength Data</th>
                  <th>Reference Source</th>
                </tr>
              </thead>

              <tbody>
                {recommendations.map((material) => (
                  <tr key={material.material_code}>
                    <td>{material.name}</td>

                    <td>{material.grade}</td>

                    <td>
                      {material.density.toLocaleString()}
                    </td>

                    <td>
                      ${material.price_per_kg.toFixed(2)}
                    </td>

                    <td>
                      {displayStrength(
                        material.yield_strength_min_mpa
                      )}
                    </td>

                    <td>
                      {displayStrength(
                        material.tensile_strength_mpa
                      )}
                    </td>

                    <td>
                      {displayStrengthType(
                        material.strength_data_type
                      )}
                    </td>

                    <td>
                      {material.strength_source ||
                        "Not specified"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      <p style={{ fontSize: "12px", marginTop: "16px" }}>
        Engineering reference notice: Strength values
        depend on grade, product form, condition, and
        applicable specification. Prices and machine
        limits are demonstration data. Recommendations
        are preliminary screening results, not approval
        for manufacturing or structural design.
      </p>
    </section>
  );
}

export default MaterialRecommendation;
