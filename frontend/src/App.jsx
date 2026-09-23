import { useEffect, useState } from "react";

import "./App.css";

import Header from "./components/common/Header";
import Footer from "./components/common/Footer";
import Sidebar from "./components/common/Sidebar";
import DocumentUpload from "./components/common/DocumentUpload";
import Dashboard from "./components/common/Dashboard";

import ChatPanel from "./components/chat/ChatPanel";
import PredictionPanel from "./components/prediction/PredictionPanel";

function App() {
  const [activePage, setActivePage] = useState("dashboard");

  // ============================================================
  // THEME
  // ============================================================

  const [theme, setTheme] = useState(() => {
    return localStorage.getItem("theme") || "dark";
  });

  useEffect(() => {
    document.documentElement.classList.remove(
      "theme-dark",
      "theme-light"
    );

    document.documentElement.classList.add(
      `theme-${theme}`
    );

    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((currentTheme) =>
      currentTheme === "dark"
        ? "light"
        : "dark"
    );
  };

  // ============================================================
  // PAGE RENDERING
  // ============================================================

  const renderPage = () => {
    switch (activePage) {
      case "dashboard":
        return (
          <main className="main-content single-panel">
            <Dashboard onNavigate={setActivePage} />
          </main>
        );

      case "assistant":
        return (
          <main className="main-content single-panel">
            <ChatPanel />
          </main>
        );

      case "predictions":
        return (
          <main className="main-content single-panel">
            <PredictionPanel />
          </main>
        );

      case "knowledge":
        return (
          <main className="main-content single-panel">
            <DocumentUpload
              onNavigateToChat={() => setActivePage("assistant")}
            />
          </main>
        );

      case "settings":
        return (
          <main className="main-content single-panel">
            <section className="glass page-placeholder">
              <div className="panel-header">
                <div className="panel-title-row">
                  <div className="panel-icon prediction-icon">
                    ⚙
                  </div>

                  <div>
                    <h2>Settings</h2>

                    <p>
                      Configure application preferences
                      and system settings.
                    </p>
                  </div>
                </div>
              </div>

              <div className="placeholder-content">
                <h3>Appearance</h3>

                <p>
                  Choose how the application looks.
                </p>

                <div className="theme-setting">
                  <div>
                    <strong>
                      Application Theme
                    </strong>

                    <span>
                      Currently using{" "}
                      {theme === "dark"
                        ? "Dark Mode"
                        : "Light Mode"}
                    </span>
                  </div>

                  <button
                    type="button"
                    className="theme-toggle"
                    onClick={toggleTheme}
                  >
                    <span className="theme-toggle-icon">
                      {theme === "dark"
                        ? "☀"
                        : "☾"}
                    </span>

                    {theme === "dark"
                      ? "Light Mode"
                      : "Dark Mode"}
                  </button>
                </div>
              </div>
            </section>
          </main>
        );

      default:
        return (
          <main className="main-content">
            <ChatPanel />
            <PredictionPanel />
          </main>
        );
    }
  };

  // ============================================================
  // APPLICATION
  // ============================================================

  return (
    <div className="app">
      <div className="background-orb orb-one"></div>
      <div className="background-orb orb-two"></div>
      <div className="background-orb orb-three"></div>

      <Sidebar
        activePage={activePage}
        onNavigate={setActivePage}
      />

      <div className="app-shell">
        <Header
          theme={theme}
          onToggleTheme={toggleTheme}
        />

        {renderPage()}

        <Footer />
      </div>
    </div>
  );
}

export default App;