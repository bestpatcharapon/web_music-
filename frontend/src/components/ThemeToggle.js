import React, { useEffect, useState } from "react";

function ThemeToggle() {
  const [isDarkMode, setIsDarkMode] = useState(true);

  useEffect(() => {
    // Check if user has a theme preference stored
    // Only access localStorage in browser environment
    if (typeof window !== "undefined" && window.localStorage) {
      const savedTheme = localStorage.getItem("theme");
      if (savedTheme) {
        setIsDarkMode(savedTheme === "dark");
        document.body.setAttribute("data-theme", savedTheme);
      } else {
        // Default to dark theme
        document.body.setAttribute("data-theme", "dark");
      }
    } else {
      // Fallback for non-browser environments
      document.body.setAttribute("data-theme", "dark");
    }
  }, []);

  const toggleTheme = () => {
    const newTheme = isDarkMode ? "light" : "dark";
    setIsDarkMode(!isDarkMode);
    document.body.setAttribute("data-theme", newTheme);
    // Only save to localStorage in browser environment
    if (typeof window !== "undefined" && window.localStorage) {
      localStorage.setItem("theme", newTheme);
    }
  };

  return (
    <button
      className="theme-toggle-btn"
      onClick={toggleTheme}
      aria-label={isDarkMode ? "Switch to light mode" : "Switch to dark mode"}
    >
      {isDarkMode ? (
        <span className="theme-icon">☀️</span>
      ) : (
        <span className="theme-icon">🌙</span>
      )}
    </button>
  );
}

export default ThemeToggle;
