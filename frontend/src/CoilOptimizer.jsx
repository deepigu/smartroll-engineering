
import { useState } from "react";

function CoilOptimizer() {
  const [requiredWeight, setRequiredWeight] = useState("");
  const [pricePerKg, setPricePerKg] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const formatNumber = (value) =>
    Number(value).toLocaleString("en-CA", {
      maximumFractionDigits: 2,
    });

  const formatCurrency = (value) =>
    Number(value).toLocaleString("en-CA", {
      style: "currency",
      currency: "CAD",
    });

  async function handleOptimize(event) {
    event.preventDefault();

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/optimize-coils",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            required_weight: Number(requiredWeight),
            price_per_kg: Number(pricePerKg),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : "Coil optimization failed."
        );
      }

      setResult(data.result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  const savings = result
    ? result.best_option.total_cost -
      result.best_mixed_option.total_cost
    : 0;

  return (
    <section className="recommendation-section">
      <h2>Intelligent Coil Optimization</h2>

      <p>
        Compare coil purchasing options and identify
        combinations that minimize purchased material.
      </p>

      <form
        className="recommendation-form"
        onSubmit={handleOptimize}
      >
        <div>
          <label htmlFor="required-weight">
            Required Material Weight (kg)
          </label>

          <input
            id="required-weight"
            type="number"
            min="0.01"
            step="any"
            placeholder="Example: 11000"
            value={requiredWeight}
            onChange={(event) =>
              setRequiredWeight(event.target.value)
            }
            required
          />
        </div>

        <div>
          <label htmlFor="coil-price">
            Material Price per kg (CAD)
          </label>

          <input
            id="coil-price"
            type="number"
            min="0"
            step="any"
            placeholder="Example: 1.50"
            value={pricePerKg}
            onChange={(event) =>
              setPricePerKg(event.target.value)
            }
            required
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading
            ? "Optimizing Coils..."
            : "Optimize Coil Selection"}
        </button>
      </form>

      {error && (
        <p role="alert" style={{ color: "#b91c1c" }}>
          {error}
        </p>
      )}

      {result && (
        <div>
          <h3>Optimization Results</h3>

          <div className="dashboard-cards">
            <div className="dashboard-card">
              <h4>Required Weight</h4>
              <p>
                {formatNumber(result.required_weight)} kg
              </p>
            </div>

            <div className="dashboard-card">
              <h4>Best Mixed-Coil Cost</h4>
              <p>
                {formatCurrency(
                  result.best_mixed_option.total_cost
                )}
              </p>
            </div>

            <div className="dashboard-card">
              <h4>Potential Savings</h4>
              <p>{formatCurrency(savings)}</p>
            </div>

            <div className="dashboard-card">
              <h4>Material Utilization</h4>
              <p>
                {formatNumber(
                  result.best_mixed_option
                    .utilization_percentage
                )}
                %
              </p>
            </div>
          </div>

          <h3>Single-Size Coil Comparison</h3>

          <div style={{ overflowX: "auto" }}>
            <table>
              <thead>
                <tr>
                  <th>Coil Type</th>
                  <th>Coils Needed</th>
                  <th>Purchased Weight</th>
                  <th>Remaining Weight</th>
                  <th>Utilization</th>
                  <th>Total Cost</th>
                </tr>
              </thead>

              <tbody>
                {result.options.map((option) => (
                  <tr key={option.coil_name}>
                    <td>{option.coil_name}</td>
                    <td>{option.coils_needed}</td>
                    <td>
                      {formatNumber(
                        option.purchased_weight
                      )} kg
                    </td>
                    <td>
                      {formatNumber(
                        option.remaining_weight
                      )} kg
                    </td>
                    <td>
                      {formatNumber(
                        option.utilization_percentage
                      )}%
                    </td>
                    <td>
                      {formatCurrency(option.total_cost)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <h3>Recommended Mixed-Coil Combination</h3>

          <div style={{ overflowX: "auto" }}>
            <table>
              <thead>
                <tr>
                  <th>Coil Type</th>
                  <th>Weight per Coil</th>
                  <th>Quantity</th>
                </tr>
              </thead>

              <tbody>
                {result.best_mixed_option.coil_combination.map(
                  (coil) => (
                    <tr key={coil.coil_name}>
                      <td>{coil.coil_name}</td>
                      <td>
                        {formatNumber(
                          coil.coil_weight_kg
                        )} kg
                      </td>
                      <td>{coil.quantity}</td>
                    </tr>
                  )
                )}
              </tbody>
            </table>
          </div>

          <p>
            <strong>Total Coils:</strong>{" "}
            {result.best_mixed_option.total_coils}
          </p>

          <p>
            <strong>Remaining Material:</strong>{" "}
            {formatNumber(
              result.best_mixed_option.remaining_weight
            )} kg
          </p>

          <p>
            <strong>Best Mixed-Coil Purchase:</strong>{" "}
            {formatCurrency(
              result.best_mixed_option.total_cost
            )}
          </p>

          <p>
            <strong>Potential Savings:</strong>{" "}
            {formatCurrency(savings)}
          </p>

          <h4>Planning Assumptions</h4>
          <ul>
            {result.assumptions.map((assumption, index) => (
              <li key={index}>{assumption}</li>
            ))}
          </ul>
        </div>
      )}

      <p style={{ fontSize: "12px", marginTop: "16px" }}>
        Note: Coil sizes and material prices are
        demonstration inputs. Results estimate
        purchasing quantities and remaining inventory,
        not actual roll-forming scrap or certified
        production savings.
      </p>
    </section>
  );
}

export default CoilOptimizer;
