import { useEffect, useState } from "react";

import { getDocuments } from "../../services/api";

const Dashboard = ({ onNavigate }) => {
  const [documentCount, setDocumentCount] = useState(null);

  useEffect(() => {
    const loadStats = async () => {
      try {
        const response = await getDocuments();

        const documents = Array.isArray(response)
          ? response
          : response?.documents || [];

        setDocumentCount(documents.length);
      } catch (err) {
        console.error("Failed to load dashboard stats:", err);
        setDocumentCount(null);
      }
    };

    loadStats();
  }, []);

  const cards = [
    {
      id: "assistant",
      icon: "✦",
      title: "AI Assistant",
      description:
        "Chat with the AI assistant and get grounded answers from your documents.",
      cta: "Open Assistant →",
    },
    {
      id: "predictions",
      icon: "◇",
      title: "Predictions",
      description:
        "Run customer churn predictions using trained ML models.",
      cta: "Open Predictions →",
    },
    {
      id: "knowledge",
      icon: "📄",
      title: "Knowledge Base",
      description:
        documentCount !== null
          ? `${documentCount} document${
              documentCount === 1 ? "" : "s"
            } indexed and searchable.`
          : "Upload documents for AI knowledge retrieval.",
      cta: "Manage Documents →",
    },
  ];

  return (
    <section className="glass dashboard-panel">
      {/* -------------------------------------------------- */}
      {/* HEADER */}
      {/* -------------------------------------------------- */}

      <div className="panel-header">
        <div className="panel-title-row">
          <div className="panel-icon prediction-icon">
            ◈
          </div>

          <div>
            <h2>Customer Churn AI</h2>

            <p>
              Your ML-powered customer intelligence platform.
              Choose where to start below.
            </p>
          </div>
        </div>
      </div>

      {/* -------------------------------------------------- */}
      {/* NAVIGATION CARDS */}
      {/* -------------------------------------------------- */}

      <div className="dashboard-cards">
        {cards.map((card) => (
          <button
            key={card.id}
            type="button"
            className="dashboard-card"
            onClick={() => onNavigate(card.id)}
          >
            <div className="dashboard-card-icon">
              {card.icon}
            </div>

            <div className="dashboard-card-body">
              <h3>{card.title}</h3>
              <p>{card.description}</p>
            </div>

            <div className="dashboard-card-cta">
              {card.cta}
            </div>
          </button>
        ))}
      </div>

      {/* -------------------------------------------------- */}
      {/* STATUS */}
      {/* -------------------------------------------------- */}

      <div className="dashboard-status">
        <div className="status-dot"></div>
        <span>All systems connected — AI, prediction, and retrieval services are running.</span>
      </div>
    </section>
  );
};

export default Dashboard;