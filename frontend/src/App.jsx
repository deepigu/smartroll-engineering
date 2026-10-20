
import { useEffect, useState } from "react";
import {
  LayoutDashboard,
  Layers,
  Sparkles,
  CircleGauge,
  ClipboardList,
  PackageCheck,
  Settings,
  Menu,
  ArrowRight,
} from "lucide-react";

import OrderForm from "./OrderForm";
import MaterialSelection from "./MaterialSelection";
import MaterialRecommendation from "./MaterialRecommendation";
import CoilOptimizer from "./CoilOptimizer";
import ProductionPlanner from "./ProductionPlanner";
import "./App.css";

const API_BASE =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const menuItems = [
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "materials", label: "Materials", icon: Layers },
  { id: "recommendations", label: "Recommendations", icon: Sparkles },
  { id: "coils", label: "Coil Optimization", icon: CircleGauge },
  { id: "planning", label: "Production Planning", icon: ClipboardList },
  { id: "orders", label: "Production Orders", icon: PackageCheck },
];

function App() {
  const [activePage, setActivePage] = useState("dashboard");
  const [orders, setOrders] = useState([]);
  const [refreshOrders, setRefreshOrders] = useState(0);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    async function loadOrders() {
      try {
        setLoading(true);
        setError("");

        const response = await fetch(`${API_BASE}/orders`);

        if (!response.ok) {
          throw new Error(
            `Failed to fetch production orders (HTTP ${response.status})`
          );
        }

        const data = await response.json();

        const orderList = Array.isArray(data)
          ? data
          : data.orders;

        if (!Array.isArray(orderList)) {
          throw new Error("Unexpected orders response");
        }

        setOrders(orderList);
      } catch (err) {
        console.error("API Error:", err);
        setError("Unable to load production orders. Check FastAPI.");
      } finally {
        setLoading(false);
      }
    }

    loadOrders();
  }, [refreshOrders]);

  function navigate(page) {
    setActivePage(page);
    setMenuOpen(false);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  const currentPage =
    menuItems.find((item) => item.id === activePage) ||
    menuItems[0];

  function renderOrdersTable() {
    return (
      <section className="orders-section">
        <h2>Production Orders</h2>

        <div className="table-scroll">
          <table className="orders-table">
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Material</th>
                <th>Machine</th>
                <th>Quantity</th>
                <th>Part Length (m)</th>
              </tr>
            </thead>

            <tbody>
              {orders.map((order) => (
                <tr key={order.id ?? order.order_id}>
                  <td>{order.order_id}</td>
                  <td>{order.material_code}</td>
                  <td>{order.machine_code}</td>
                  <td>{order.quantity}</td>
                  <td>{order.part_length}</td>
                </tr>
              ))}

              {loading && (
                <tr>
                  <td colSpan="5">Loading production orders...</td>
                </tr>
              )}

              {!loading && !error && orders.length === 0 && (
                <tr>
                  <td colSpan="5">No production orders found.</td>
                </tr>
              )}

              {!loading && error && (
                <tr>
                  <td colSpan="5">{error}</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    );
  }

  return (
    <div className="app-layout">
      <aside className={`sidebar ${menuOpen ? "sidebar-open" : ""}`}>
        <div className="brand">
          <div className="brand-icon">
            <Settings size={25} />
          </div>

          <div>
            <h2>SmartRoll</h2>
            <p>Engineering Platform</p>
          </div>
        </div>

        <div className="sidebar-label">WORKSPACE</div>

        <nav aria-label="Main navigation">
          {menuItems.map((item) => {
            const Icon = item.icon;

            return (
              <button
                key={item.id}
                type="button"
                className={
                  activePage === item.id
                    ? "nav-item active"
                    : "nav-item"
                }
                onClick={() => navigate(item.id)}
              >
                <span className="nav-icon">
                  <Icon size={19} strokeWidth={1.8} />
                </span>
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="sidebar-footer">
          <span className="status-dot" />
          SmartRoll v1.3
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <button
            type="button"
            className="mobile-menu-button"
            onClick={() => setMenuOpen(!menuOpen)}
            aria-label="Toggle navigation"
          >
            <Menu size={23} />
          </button>

          <div>
            <p className="eyebrow">SMARTROLL / WORKSPACE</p>
            <h1>{currentPage.label}</h1>
          </div>

          <span className="topbar-badge">
            Engineering Workspace
          </span>
        </header>

        {activePage === "dashboard" && (
          <>
            <p className="page-description">
              Intelligent roll-forming material selection,
              purchasing optimization, and production management.
            </p>

            <div className="dashboard-cards">
              <div className="card">
                <h3>Materials</h3>
                <h2>4</h2>
                <p>Demo material grades</p>
              </div>

              <div className="card">
                <h3>Machines</h3>
                <h2>2</h2>
                <p>Demo machine profiles</p>
              </div>

              <div className="card">
                <h3>Production Orders</h3>
                <h2>
                  {loading
                    ? "..."
                    : error
                      ? "N/A"
                      : orders.length}
                </h2>
                <p>Saved in PostgreSQL</p>
              </div>

              <div className="card">
                <h3>Database Connection</h3>
                <h2 className="connection-status">
                  {loading
                    ? "Checking"
                    : error
                      ? "Unavailable"
                      : "Connected"}
                </h2>
                <p>Production order service</p>
              </div>
            </div>

            <section className="overview-section">
              <h2>Engineering Tools</h2>
              <p>Choose a tool to start working.</p>

              <div className="tool-grid">
                {menuItems
                  .filter((item) => item.id !== "dashboard")
                  .map((item) => {
                    const Icon = item.icon;

                    return (
                      <button
                        key={item.id}
                        type="button"
                        className="tool-card"
                        onClick={() => navigate(item.id)}
                      >
                        <span className="tool-icon">
                          <Icon size={22} strokeWidth={1.8} />
                        </span>

                        <strong>{item.label}</strong>

                        <span className="tool-arrow">
                          <ArrowRight size={18} />
                        </span>
                      </button>
                    );
                  })}
              </div>
            </section>

            {renderOrdersTable()}
          </>
        )}

        {activePage === "materials" && <MaterialSelection />}

        {activePage === "recommendations" && (
          <MaterialRecommendation />
        )}

        {activePage === "coils" && <CoilOptimizer />}

        {activePage === "planning" && <ProductionPlanner />}

        {activePage === "orders" && (
          <>
            {renderOrdersTable()}

            <OrderForm
              onOrderCreated={() =>
                setRefreshOrders((count) => count + 1)
              }
            />
          </>
        )}
      </main>
    </div>
  );
}

export default App;
