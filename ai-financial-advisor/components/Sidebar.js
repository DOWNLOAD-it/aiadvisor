"use client";
import { useState } from "react";

export default function Sidebar({ onAnalyze, isLoading }) {
  const [formData, setFormData] = useState({
    currency: "MAD",
    age: 30,
    income: 15000,
    occupation: "Professional",
    city_tier: "Tier_1",
    desired_savings_pct: 20,
    groceries: 3000,
    transport: 1000,
    eating_out: 1500,
    entertainment: 800,
    utilities: 1200,
    misc: 1000,
  });

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "number" ? parseFloat(value) || 0 : value,
    }));
  };

  return (
    <div className="sidebar">
      <div className="brand">
        <div className="bg-primary text-white rounded p-1">
          <i className="bi bi-wallet2 fs-5"></i>
        </div>
        <h5 className="mb-0 fw-bold text-dark">FinAdvisor</h5>
      </div>

      <form className="d-flex flex-column gap-3">
        {/* Profile Section */}
        <div>
          <label className="text-secondary fw-bold small mb-2 text-uppercase">
            Profile
          </label>
          <div className="row g-2">
            <div className="col-6">
              <label className="form-label">Currency</label>
              <select
                className="form-select"
                name="currency"
                value={formData.currency}
                onChange={handleChange}
              >
                <option value="MAD">MAD</option>
                <option value="USD">USD</option>
                <option value="INR">INR</option>
              </select>
            </div>
            <div className="col-6">
              <label className="form-label">Income</label>
              <input
                type="number"
                className="form-control"
                name="income"
                value={formData.income}
                onChange={handleChange}
              />
            </div>
          </div>
          <div className="row g-2 mt-1">
            <div className="col-6">
              <label className="form-label">Occupation</label>
              <select
                className="form-select"
                name="occupation"
                value={formData.occupation}
                onChange={handleChange}
              >
                <option value="Professional">Pro</option>
                <option value="Student">Student</option>
              </select>
            </div>
            <div className="col-6">
              <label className="form-label">Goal %</label>
              <input
                type="number"
                className="form-control"
                name="desired_savings_pct"
                value={formData.desired_savings_pct}
                onChange={handleChange}
              />
            </div>
          </div>
        </div>

        <hr className="my-1 border-secondary opacity-25" />

        {/* Expenses Section */}
        <div>
          <label className="text-secondary fw-bold small mb-2 text-uppercase">
            Expenses
          </label>
          <div className="row g-2">
            {[
              "groceries",
              "transport",
              "eating_out",
              "entertainment",
              "utilities",
              "misc",
            ].map((f) => (
              <div className="col-6" key={f}>
                <label
                  className="form-label text-capitalize"
                  style={{ fontSize: "0.75rem" }}
                >
                  {f.replace("_", " ")}
                </label>
                <input
                  type="number"
                  className="form-control form-control-sm"
                  name={f}
                  value={formData[f]}
                  onChange={handleChange}
                />
              </div>
            ))}
          </div>
        </div>

        <button
          type="button"
          className="btn btn-primary w-100 mt-auto shadow-sm"
          onClick={() => onAnalyze(formData)}
          disabled={isLoading}
        >
          {isLoading ? "Processing..." : "Analyze Now"}
        </button>
      </form>
    </div>
  );
}
