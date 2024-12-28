import React, { useEffect, useState } from 'react';
import './Catalogue.css';

interface Pet {
  name: string; // Use name for identification
  age: string; // Age is now a string
  breed: string;
  location: string; // Location is required for uniqueness
  picture_url?: string;
}

interface CatalogueProps {
  userEmail: string;
  onEdit: (petName: string) => void; // Pass pet name for editing
  onNavigate: (screen: string) => void; // Function to navigate between screens
}

export default function Catalogue({ userEmail, onEdit, onNavigate }: CatalogueProps) {
  const [pets, setPets] = useState<Pet[]>([]);
  const [filteredPets, setFilteredPets] = useState<Pet[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Filter states
  const [selectedBreed, setSelectedBreed] = useState<string>('Any');
  const [selectedAge, setSelectedAge] = useState<string>('Any');
  const [selectedSize, setSelectedSize] = useState<string>('Any');
  const [selectedGender, setSelectedGender] = useState<string>('Any');
  const [selectedCare, setSelectedCare] = useState<string>('Any');

  const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:5000';

  // Check if the user is an admin based on their email domain
  const isAdmin = userEmail.endsWith('@admin.com');

  useEffect(() => {
    setLoading(true);
    fetch(`${backendUrl}/pets`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        setPets(data.pets);
        setFilteredPets(data.pets); // Initialize filteredPets
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching pets:', error);
        setError('Failed to fetch pets data');
        setLoading(false);
      });
  }, [backendUrl]);

  useEffect(() => {
    let updatedPets = pets;

    if (selectedBreed !== 'Any') {
      updatedPets = updatedPets.filter((pet) => pet.breed === selectedBreed);
    }

    if (selectedAge !== 'Any') {
      updatedPets = updatedPets.filter((pet) => {
        if (selectedAge === 'Young') return parseInt(pet.age) <= 2;
        if (selectedAge === 'Old') return parseInt(pet.age) > 2;
        return true;
      });
    }

    setFilteredPets(updatedPets);
  }, [selectedBreed, selectedAge, selectedSize, selectedGender, selectedCare, pets]);

  const handleAddToFavorites = (petName: string) => {
    console.log("Adding to favorites with email:", userEmail); // Log the email
    console.log("Adding pet:", petName);
    fetch(`${backendUrl}/favorites`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: userEmail, // Send the user's email
        pet_name: petName, // Send the pet's name
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to add pet to favorites');
        }
        return response.json();
      })
      .then((data) => {
        console.log("Favorite added response:", data); // Log the response
        alert(data.message || 'Pet added to favorites!');
      })
      .catch((error) => {
        console.error('Error adding pet to favorites:', error);
        alert('Failed to add pet to favorites. Please try again.');
      });
};


  const renderPetCards = () => {
    if (filteredPets.length === 0) {
      return <p>No pets match your criteria.</p>;
    }
    return filteredPets.map((pet) => (
      <div className="pet-card" key={`${pet.name}-${pet.location}`}>
        <img src={pet.picture_url || '/default-pet.jpg'} alt={pet.name} />
        <div
          className="favorite-icon"
          onClick={() => handleAddToFavorites(pet.name, pet.location)} // Add to favorites using name and location
          title="Add to Favorites"
        >
          ❤️
        </div>
        <h3>{pet.name}</h3>
        <p>{pet.age} years old</p>
        <p>{pet.breed}</p>
        <p className="location">{pet.location || 'Location unknown'}</p>
        {isAdmin && (
          <button className="edit-button" onClick={() => onEdit(pet.name)}>
            Edit Information
          </button>
        )}
      </div>
    ));
  };

  return (
    <div>
      <div id="dropdownSection">
        <div className="header">ADOPTAPET Catalog</div>
        <div className="find-your-match">
          <h5>Find Your Best Match!</h5>

          <p>Breed</p>
          <select className="dropdown" value={selectedBreed} onChange={(e) => setSelectedBreed(e.target.value)}>
            <option>Any</option>
            <option>Lab</option>
            <option>Beagle</option>
            <option>Golden Retriever</option>
            <option>Persian</option>
            <option>German Shepherd</option>
            <option>Tabby</option>
          </select>

          <p>Age</p>
          <select className="dropdown" value={selectedAge} onChange={(e) => setSelectedAge(e.target.value)}>
            <option>Any</option>
            <option>Young</option>
            <option>Old</option>
          </select>

          <p>Size</p>
          <select className="dropdown" value={selectedSize} onChange={(e) => setSelectedSize(e.target.value)}>
            <option>Any</option>
            <option>Small</option>
            <option>Medium</option>
            <option>Large</option>
          </select>

          <p>Gender</p>
          <select className="dropdown" value={selectedGender} onChange={(e) => setSelectedGender(e.target.value)}>
            <option>Any</option>
            <option>Male</option>
            <option>Female</option>
          </select>

          <p>Care & Behaviour</p>
          <select className="dropdown" value={selectedCare} onChange={(e) => setSelectedCare(e.target.value)}>
            <option>Any</option>
            <option>Low</option>
            <option>Medium</option>
            <option>High</option>
          </select>
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <div className="catalog-container">
          {loading && <p>Loading...</p>}
          {error && <p>{error}</p>}
          {!loading && !error && renderPetCards()}
        </div>
        {userEmail.endsWith('@admin.com') && (
          <button
            className="add-button"
            onClick={() => onNavigate('add')}
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
        )}
      </div>


    </div>
  );
}
