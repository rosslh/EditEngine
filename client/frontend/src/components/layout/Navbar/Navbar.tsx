import React from "react";
import { NavLink, Link } from "react-router-dom";
import "./Navbar.scss";

const Navbar: React.FC = () => {
  return (
    <nav className="navbar" role="navigation" aria-label="Main navigation">
      <div className="navbar__container">
        <Link to="/" className="navbar__logo" aria-label="Go to main edit page">
          <img src="/logo/wordmark.png" alt="EditEngine" height={32} />
        </Link>
        <div className="navbar__tabs">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `navbar__tab ${isActive ? "navbar__tab--active" : ""}`
            }
            end
          >
            New
          </NavLink>
          <NavLink
            to="/history"
            className={({ isActive }) =>
              `navbar__tab ${isActive ? "navbar__tab--active" : ""}`
            }
          >
            History
          </NavLink>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
