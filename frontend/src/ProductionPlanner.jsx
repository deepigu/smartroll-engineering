
import { useState } from "react";

const API_BASE =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const initialForm = {
  quantity: "1500",
  part_length_m: "2.5",
  strip_width_mm: "400",
  thickness_mm: "1.5",
  density: "7850",
  price_per_kg: "1.5",
  production_speed_m_min: "20",
  setup_time_min: "30",
  waste_percentage: "5",
};

const fields = [
  { name: "quantity", label: "Production Quantity (parts)", min: "1", step: "1" },
  { name: "part_length_m", label: "Part Length (m)", min: "0.001", step: "any" },
  { name: "strip_width_mm", label: "Strip Width (mm)", min: "0.001", step: "any" },
  { name: "thickness_mm", label: "Material Thickness (mm)", min: "0.001", step: "any" },
  { name: "density", label: "Material Density (kg/m³)", min: "0.001", step: "any" },
  { name: "price_per_kg", label: "Material Price (CAD/kg)", min: "0", step: "any" },
  { name: "production_speed_m_min", label: "Production Speed (m/min)", min: "0.001", step: "any" },
  { name: "setup_time_min", label: "Machine Setup Time (minutes)", min: "0", step: "any" },
  { name: "waste_percentage", label: "Estimated Waste (%)", min: "0", max: "99.99", step: "any" },
];

function ProductionPlanner() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [planInputs, setPlanInputs] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [downloading, setDownloading] = useState(false);

  const formatNumber = (value) =>
    Number(value).toLocaleString("en-CA", {
      maximumFractionDigits: 2,
    });

  const formatCurrency = (value) =>
    Number(value).toLocaleString("en-CA", {
      style: "currency",
      currency: "CAD",
    });

  function getPayload() {
    return Object.fromEntries(
      Object.entries(form).map(([key, value]) => [
        key,
        Number(value),
      ])
    );
  }

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));

    // Prevent downloading an outdated report after inputs change.
    setResult(null);
    setPlanInputs(null);
    setError("");
  }

  async function readApiError(response) {
    try {
      const data = await response.json();

      if (typeof data.detail === "string") {
        return data.detail;
      }
    } catch {
      // Use the fallback message below.
    }

    return `Request failed (HTTP ${response.status}).`;
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setLoading(true);
    setError("");
    setResult(null);
    setPlanInputs(null);

    const payload = getPayload();

    try {
      const response = await fetch(
        `${API_BASE}/plan-production`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        }
      );

      if (!response.ok) {
        throw new Error(await readApiError(response));
      }

      const data = await response.json();

      setResult(data.result);
      setPlanInputs(payload);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleDownload() {
    if (!planInputs || downloading) {
      return;
    }

    setDownloading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_BASE}/production-report`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(planInputs),
        }
      );

      if (!response.ok) {
        throw new Error(await readApiError(response));
      }

      const pdfBlob = await response.blob();

      const url = URL.createObjectURL(pdfBlob);

      const link = document.createElement("a");
      link.href = url;
      link.download = "SmartRoll_Production_Report.pdf";

      document.body.appendChild(link);
      link.click();
      link.remove();

      setTimeout(() => {
        URL.revokeObjectURL(url);
      }, 1000);
    } catch (err) {
      setError(err.message);
    } finally {
      setDownloading(false);
    }
  }

  const metrics = result
    ? [
        ["Production Quantity", `${formatNumber(result.quantity)} parts`],
        ["Total Material Length", `${formatNumber(result.total_length_m)} m`],
        ["Net Material Weight", `${formatNumber(result.net_weight_kg)} kg`],
        ["Gross Material Weight", `${formatNumber(result.gross_weight_kg)} kg`],
        ["Estimated Material Waste", `${formatNumber(result.estimated_waste_kg)} kg`],
        ["Material Cost", formatCurrency(result.material_cost)],
        ["Production Run Time", `${formatNumber(result.run_time_min)} min`],
        ["Machine Setup Time", `${formatNumber(result.setup_time_min)} min`],
        ["Total Production Time", `${formatNumber(result.total_time_min)} min`],
        ["Estimated 8-Hour Shifts", result.estimated_shifts_8h],
      ]
    : [];

  return (
    <section className="recommendation-section">
      <h2>Intelligent Production Planner</h2>

      <p>
        Estimate material requirements, production duration,
        purchasing costs, and shift requirements.
      </p>

      <form
        className="recommendation-form"
        onSubmit={handleSubmit}
      >
        {fields.map((field) => (
          <div key={field.name}>
            <label htmlFor={field.name}>
              {field.label}
            </label>

            <input
              id={field.name}
              name={field.name}
              type="number"
              min={field.min}
              max={field.max}
              step={field.step}
              value={form[field.name]}
              onChange={handleChange}
              required
            />
          </div>
        ))}

        <button type="submit" disabled={loading}>
          {loading
            ? "Generating Plan..."
            : "Generate Production Plan"}
        </button>
      </form>

      {error && (
        <p role="alert" style={{ color: "#b91c1c" }}>
          {error}
        </p>
      )}

      {result && (
        <div>
          <h3>Production Planning Results</h3>

          <div className="dashboard-cards">
            <div className="card">
              <h3>Gross Material</h3>
              <h2>
                {formatNumber(result.gross_weight_kg)} kg
              </h2>
            </div>

            <div className="card">
              <h3>Material Cost</h3>
              <h2>
                {formatCurrency(result.material_cost)}
              </h2>
            </div>

            <div className="card">
              <h3>Production Duration</h3>
              <h2>
                {formatNumber(result.total_time_hours)} hrs
              </h2>
            </div>

            <div className="card">
              <h3>Estimated Shifts</h3>
              <h2>{result.estimated_shifts_8h}</h2>
            </div>
          </div>

          <h3>Detailed Production Breakdown</h3>

          <div style={{ overflowX: "auto" }}>
            <table className="orders-table">
              <thead>
                <tr>
                  <th>Production Metric</th>
                  <th>Estimated Value</th>
                </tr>
              </thead>

              <tbody>
                {metrics.map(([label, value]) => (
                  <tr key={label}>
                    <td>{label}</td>
                    <td>{value}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <h3>Engineering Assumptions</h3>

          <ul>
            {result.assumptions.map((assumption, index) => (
              <li key={index}>{assumption}</li>
            ))}
          </ul>

          <button
            type="button"
            onClick={handleDownload}
            disabled={downloading}
            style={{ marginTop: "16px" }}
          >
            {downloading
              ? "Generating PDF..."
              : "Download PDF Engineering Report"}
          </button>

          <p style={{ fontSize: "12px", marginTop: "16px" }}>
            Preliminary planning estimates only.
            Not a certified engineering or manufacturing approval.
          </p>
        </div>
      )}
    </section>
  );
}

export default ProductionPlanner;
