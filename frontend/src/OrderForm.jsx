
import { useState } from "react";

function OrderForm({ onOrderCreated }) {
  const [orderId, setOrderId] = useState("");
  const [material, setMaterial] = useState("cs_type_b");
  const [machine, setMachine] = useState("RF100");
  const [quantity, setQuantity] = useState("");
  const [partLength, setPartLength] = useState("");

const [message, setMessage] = useState("");
const [saving, setSaving] = useState(false);

async function handleSubmit(event) {
  event.preventDefault();

  setSaving(true);
  setMessage("");

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/orders",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          order_id: orderId.trim(),
          material_code: material,
          machine_code: machine,
          quantity: Number(quantity),
          part_length: Number(partLength)
        })
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        typeof data.detail === "string"
          ? data.detail
          : "Unable to create production order"
      );
    }

    setMessage("Production order created successfully!");
onOrderCreated();
    // Clear the form after successful submission
    setOrderId("");
    setQuantity("");
    setPartLength("");

  } catch (error) {
    setMessage(`Error: ${error.message}`);
  } finally {
    setSaving(false);
  }
}

 
  return (
    <section className="orders-section">
      <h2>Create Production Order</h2>

      <form onSubmit={handleSubmit}>

        <div className="form-field">
          <label htmlFor="order-id">Order ID</label>
          <input
            id="order-id"
            type="text"
            placeholder="Example: ORD1004"
            value={orderId}
            onChange={(event) => setOrderId(event.target.value)}
            required
          />
        </div>

        <div className="form-field">
          <label htmlFor="material">Material</label>
          <select
            id="material"
            value={material}
            onChange={(event) => setMaterial(event.target.value)}
          >
            <option value="cs_type_b">Carbon Steel Type B</option>
            <option value="galvanized_cs">Galvanized Steel</option>
            <option value="ss304">Stainless Steel 304</option>
            <option value="al5052">Aluminum 5052</option>
          </select>
        </div>

        <div className="form-field">
          <label htmlFor="machine">Machine</label>
          <select
            id="machine"
            value={machine}
            onChange={(event) => setMachine(event.target.value)}
          >
            <option value="RF100">RF100</option>
            <option value="RF200">RF200</option>
          </select>
        </div>

        <div className="form-field">
          <label htmlFor="quantity">Quantity</label>
          <input
            id="quantity"
            type="number"
            min="1"
            placeholder="Example: 5000"
            value={quantity}
            onChange={(event) => setQuantity(event.target.value)}
            required
          />
        </div>

        <div className="form-field">
          <label htmlFor="part-length">Part Length (m)</label>
          <input
            id="part-length"
            type="number"
            min="0.01"
            step="any"
            placeholder="Example: 2.5"
            value={partLength}
            onChange={(event) => setPartLength(event.target.value)}
            required
          />
        </div>

        <button type="submit" disabled={saving}>
  {saving ? "Saving..." : "Create Order"}
</button>

      </form>
      {message && (
  <p role="status" style={{ marginTop: "15px" }}>
    {message}
  </p>
)}
    </section>
  );
}

export default OrderForm;
