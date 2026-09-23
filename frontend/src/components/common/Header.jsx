const Header = ({
  theme,
  onToggleTheme,
}) => {
  return (
    <header className="header glass">
      <div className="brand">
        <div className="brand-icon">
          ◈
        </div>

        <div>
          <h1>Customer Churn AI</h1>

          <p>
            ML-powered customer intelligence platform
          </p>
        </div>
      </div>

      <div className="header-actions">
        <button
          type="button"
          className="theme-toggle"
          onClick={onToggleTheme}
          title="Toggle application theme"
        >
          <span className="theme-toggle-icon">
            {theme === "dark" ? "☀" : "☾"}
          </span>

          <span>
            {theme === "dark"
              ? "Light"
              : "Dark"}
          </span>
        </button>

        <div className="status-pill">
          <span className="status-dot"></span>

          <span>AI Assistant</span>

          <span className="status-live">
            LIVE
          </span>
        </div>
      </div>
    </header>
  );
};

export default Header;