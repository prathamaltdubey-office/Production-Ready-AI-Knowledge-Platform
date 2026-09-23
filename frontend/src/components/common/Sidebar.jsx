const Sidebar = ({ activePage, onNavigate }) => {
  const menuItems = [
    {
      id: "dashboard",
      label: "Dashboard",
      icon: "◉",
    },
    {
      id: "assistant",
      label: "AI Assistant",
      icon: "✦",
    },
    {
      id: "predictions",
      label: "Predictions",
      icon: "◇",
    },
    {
      id: "knowledge",
      label: "Knowledge Base",
      icon: "📄",
    },
    {
      id: "settings",
      label: "Settings",
      icon: "⚙",
    },
  ];

  return (
    <aside className="sidebar glass">
      {/* BRAND */}
      <div className="sidebar-brand">
        <div className="sidebar-brand-icon">
          ◈
        </div>

        <div>
          <h2>Customer Churn AI</h2>
          <p>AI INTELLIGENCE</p>
        </div>
      </div>

      {/* NAVIGATION */}
      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <button
            key={item.id}
            type="button"
            className={`sidebar-item ${
              activePage === item.id ? "active" : ""
            }`}
            onClick={() => onNavigate(item.id)}
          >
            <span className="sidebar-item-icon">
              {item.icon}
            </span>

            <span className="sidebar-item-label">
              {item.label}
            </span>
          </button>
        ))}
      </nav>

      {/* SYSTEM STATUS */}
      <div className="sidebar-status">
        <div className="status-dot"></div>

        <div>
          <strong>System Online</strong>
          <span>AI services connected</span>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;