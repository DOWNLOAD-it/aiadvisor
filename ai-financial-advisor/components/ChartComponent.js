"use client";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip);

export default function ChartComponent({ data, labels }) {
  const chartData = {
    labels: labels,
    datasets: [
      {
        label: "Savings",
        data: data,
        backgroundColor: "#3b82f6",
        borderRadius: 4,
        barThickness: "flex", // Auto adjust
        maxBarThickness: 30,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: "#1e293b",
        padding: 10,
        cornerRadius: 6,
        displayColors: false,
        callbacks: {
          title: () => null, // Hide title in tooltip for cleaner look
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: { color: "#f1f5f9" },
        ticks: { font: { size: 10 } },
        border: { display: false },
      },
      x: {
        grid: { display: false },
        ticks: {
          font: { size: 10 },
          autoSkip: false,
          maxRotation: 45,
          minRotation: 0,
        },
        border: { display: false },
      },
    },
  };

  return <Bar data={chartData} options={options} />;
}
