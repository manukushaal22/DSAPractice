import { NavLink } from "react-router-dom";

export default function NavTabs() {
  return (
    <nav className="tabs">
      <NavLink to="/learn">Learn</NavLink>
      <NavLink to="/" end>
        Problems
      </NavLink>
    </nav>
  );
}
