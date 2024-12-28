import React, { useState, useEffect, useCallback } from 'react';
import Login from './components/Login';
import NavBar from './components/NavBar';
import Catalogue from './components/Catalogue';
import EditPet from './components/EditPet';
import AddPet from './components/AddPet'; // Import the AddPet component
import './App.css';

// Define types for favorites
interface Favorite {
  name: string;
  age: string;
  breed: string;
  picture_url: string;
  status: string;
  type: string;
  location: string;
}

const App: React.FC = () => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [userEmail, setUserEmail] = useState<string>(''); // Initially empty, will be set on login
  const [currentScreen, setCurrentScreen] = useState<string>('home');
  const [selectedPetName, setSelectedPetName] = useState<string | null>(null); // Use pet name instead of pet ID
  const [favorites, setFavorites] = useState<Favorite[]>([]); // Replace any[] with Favorite[]
  const [loadingFavorites, setLoadingFavorites] = useState<boolean>(false);
  const [favoritesError, setFavoritesError] = useState<string | null>(null);

  const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:5000';

  // Handles user login
  const handleLogin = (email: string) => {
    setUserEmail(email);
    setIsAuthenticated(true);
    fetchFavorites(email); // Fetch favorites upon login
  };

  // Handles user logout
  const handleLogout = () => {
    setUserEmail('');
    setIsAuthenticated(false);
    setCurrentScreen('home');
    setFavorites([]); // Clear favorites on logout
  };

  // Handles navigation between screens
  const handleNavigate = (screen: string) => {
    const validScreens = ['home', 'catalog', 'status', 'add']; // Add "add" as a valid screen
    if (validScreens.includes(screen)) {
      setCurrentScreen(screen);
    } else {
      console.warn(`Invalid screen: ${screen}`);
      setCurrentScreen('home');
    }
  };

  // Handles "Edit Pet" button click in the Catalogue
  const handleEditPet = (petName: string) => {
    setSelectedPetName(petName); // Set the selected pet name
    setCurrentScreen('edit');
  };

  // Handles navigation back to the Catalogue from the EditPet page
  const handleBackToCatalogue = () => {
    setSelectedPetName(null); // Clear selected pet name
    setCurrentScreen('catalog');
  };

  // Handles navigation back to the Catalogue from the AddPet page
  const handleBackToAdd = () => {
    setCurrentScreen('catalog');
  };

  // Fetch user's favorites from the backend
  const fetchFavorites = useCallback((email: string) => {
    setLoadingFavorites(true);
    fetch(`${backendUrl}/favorites?email=${email}`, {
      method: 'GET',
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to fetch favorites.');
        }
        return response.json();
      })
      .then((data) => {
        setFavorites(data.favorites || []);
        setFavoritesError(null); // Clear any previous errors
      })
      .catch((error) => {
        console.error('Error fetching favorites:', error);
        setFavoritesError('Failed to load favorites. Please try again.');
      })
      .finally(() => {
        setLoadingFavorites(false);
      });
  }, [backendUrl]);

  // Remove a pet from favorites
  const removeFavorite = (petName: string) => {
    console.debug("Attempting to remove favorite", { email: userEmail, petName }); // Debug log for deletion
  
    fetch(`${backendUrl}/favorites`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email: userEmail, pet_name: petName }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to remove pet from favorites.');
        }
        return response.json();
      })
      .then((data) => {
        console.debug("Successfully removed favorite", { email: userEmail, petName }); // Debug success log
        alert(data.message || 'Pet removed from favorites!');
        fetchFavorites(userEmail); // Refresh favorites after removal
      })
      .catch((error) => {
        console.error('Error removing pet from favorites:', error);
        alert('Failed to remove pet from favorites. Please try again.');
      });
  };
  

  // Trigger fetching favorites when the screen changes to 'home'
  useEffect(() => {
    if (currentScreen === 'home' && isAuthenticated && userEmail) {
      fetchFavorites(userEmail);
    }
  }, [currentScreen, isAuthenticated, userEmail]);

  // Render favorite cards
  const renderFavoriteCards = () => {
    if (loadingFavorites) {
      return <p>Loading favorites...</p>;
    }

    if (favoritesError) {
      return <p>{favoritesError}</p>;
    }

    if (favorites.length === 0) {
      return <p>You currently have no favorites.</p>;
    }

    return (
      <div className="favorites-container">
        {favorites.map((favorite) => (
          <div className="pet-card" key={favorite.name} style={{ position: 'relative' }}>
            <img src={favorite.picture_url || '/default-pet.jpg'} alt={favorite.name} />
            <div
              className="remove-icon"
              onClick={() => removeFavorite(favorite.name)} // Remove from favorites on click
              title="Remove from Favorites"
            >
              ❌
            </div>
            <h3>{favorite.name}</h3>
            <p>{favorite.age} years old</p>
            <p>{favorite.breed}</p>
            <p className="location">{favorite.location || 'Location unknown'}</p>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="App">
      {!isAuthenticated ? (
        // Login Screen
        <div className="login-container">
          <div className="login-box">
            <Login onLogin={handleLogin} />
          </div>
        </div>
      ) : (
        <>
          {/* Navigation Bar */}
          <NavBar onNavigate={handleNavigate} onLogout={handleLogout} />

          {/* Main Content */}
          <div className="App-content">
            {currentScreen === 'home' && (
              // Home Screen
              <div className="center-section">
                <div className="profile-section">
                  <img src="/Daniel.jpg" alt="Daniel" className="profile-picture" />
                  <div className="profile-info">
                    <h1 className="bold">Hello! Welcome to your dashboard.</h1>
                    {/* <p>Welcome to your dashboard</p> */}
                  </div>
                  <button onClick={handleLogout} className="logout-button">
                    Logout
                  </button>
                </div>
                <div className="status-section">
                  <h2 className="bold">Your Favorites</h2>
                  {renderFavoriteCards()}
                </div>
              </div>
            )}

            {currentScreen === 'catalog' && (
              // Catalogue Screen
              <div className="catalog-section">
                {/* <Catalogue userEmail={userEmail} onEdit={handleEditPet} /> */}
                <Catalogue 
                  userEmail={userEmail} 
                  onEdit={handleEditPet} 
                  onNavigate={setCurrentScreen} // Pass setCurrentScreen as onNavigate
                />
                {/* {userEmail.endsWith('@admin.com') && (
                  <button
                    className="add-button"
                    onClick={() => setCurrentScreen('add')}
                    style={{
                      marginTop: '20px',
                      padding: '10px 20px',
                      backgroundColor: '#50C462',
                      color: '#fff',
                      border: 'none',
                      borderRadius: '5px',
                      cursor: 'pointer',
                    }}
                  >
                    Add New Pet
                  </button>
                )} */}
              </div>
            )}

            {currentScreen === 'edit' && selectedPetName && (
              // EditPet Screen
              <EditPet petName={selectedPetName} onBack={handleBackToCatalogue} />
            )}

            {currentScreen === 'add' && (
              // AddPet Screen
              <AddPet onBack={handleBackToAdd} />
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default App;
