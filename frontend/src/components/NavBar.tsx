import React from 'react';
import { Navbar, Container, Nav } from 'react-bootstrap';
import './NavBar.css';

// old application status button 
// <Nav.Link onClick={() => onNavigate('status')}>Application Status</Nav.Link>

interface NavBarProps {
  onNavigate: (screen: string) => void;
  onLogout: () => void; // Logout handler
}

const NavBar: React.FC<NavBarProps> = ({ onNavigate, onLogout }) => {
  return (
    <Navbar bg="dark" variant="dark" expand="lg" fixed="top">
      <Container>
        {/* Left-aligned brand */}
        <Navbar.Brand
          onClick={() => onNavigate('home')}
          className="brand-title" // Added className for styling
        >
          ADOPTAPET
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          {/* Right-aligned navigation links */}
          <Nav className="ms-auto">
            <Nav.Link onClick={() => onNavigate('home')}>Home</Nav.Link>
            <Nav.Link onClick={() => onNavigate('catalog')}>Catalogue</Nav.Link>
            <Nav.Link
              onClick={onLogout}
              style={{
                color: 'white',
                padding: '8px 16px',
                border: '1px solid white',
                borderRadius: '4px',
                cursor: 'pointer',
                fontWeight: 'bold',
                marginLeft: '8px', // Small gap between options and Logout
              }}
            >
              Logout
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default NavBar;
