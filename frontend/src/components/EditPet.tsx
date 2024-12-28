import React, { useState, useEffect } from 'react';
import './EditPet.css';

// Define types for pet
interface Pet {
  name: string;
  age: number;
  breed: string;
  picture_url: string;
  status: string;
  type: string;
  location: string;
}

interface EditPetProps {
  petName: string; // Use pet name as the identifier
  onBack: () => void; // Callback to navigate back to the catalog
}

export default function EditPet({ petName, onBack }: EditPetProps) {
  const [formData, setFormData] = useState<Pet>({
    name: petName,
    age: 0,
    breed: '',
    picture_url: '',
    status: '',
    type: '',
    location: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:5000';

  useEffect(() => {
    setLoading(true);
    fetch(`${backendUrl}/pets`)
      .then((response) => response.json())
      .then((data) => {
        const pet = data.pets.find((p: Pet) => p.name === petName);
        if (pet) {
          setFormData(pet); // Populate formData with the pet details
        } else {
          setError('Pet not found');
        }
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to fetch pet details');
        setLoading(false);
      });
  }, [petName, backendUrl]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { id, value, type } = e.target;

    setFormData((prevFormData) => ({
      ...prevFormData,
      [id]: type === 'number' ? Number(value) : type === 'checkbox' ? (e.target as HTMLInputElement).checked : value,
    }));
  };

  const handleSave = () => {
    setLoading(true);

    const updatedFormData = { ...formData, description: 'none' };
    console.log('Parameters sent in PUT request:', updatedFormData);

    fetch(`${backendUrl}/pets`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updatedFormData),
    })
      .then((response) => {
        if (!response.ok) throw new Error('Failed to save pet details');
        alert('Pet details updated successfully!');
        onBack();
      })
      .catch(() => {
        setError('Failed to update pet details');
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const handleDelete = () => {
    if (!petName || !formData.location) {
      alert('Pet name or location not found. Unable to delete.');
      return;
    }

    if (!window.confirm('Are you sure you want to delete this pet?')) {
      return;
    }

    console.log('Attempting to delete pet with name:', petName, 'and location:', formData.location);

    setLoading(true);

    fetch(`${backendUrl}/pets`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: petName, location: formData.location }),
    })
      .then((response) => {
        console.log('Response status:', response.status);
        if (!response.ok) throw new Error('Failed to delete pet');
        alert('Pet deleted successfully!');
        onBack();
      })
      .catch((error) => {
        console.error('Error deleting pet:', error);
        setError('Failed to delete pet');
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <div className="edit-wrapper">
      <div className="edit-box">
        <h2>Edit Pet: {formData.name}</h2>
        {error && <p className="error">{error}</p>}
        <div className="pet-picture">
          <img
            src={formData.picture_url || '/default-pet.jpg'}
            alt={formData.name}
            className="pet-image"
          />
        </div>
        <div className="edit-fields">
          <div className="column">
            <div className="input-container">
              <label htmlFor="age">Age</label>
              <input
                type="text"
                id="age"
                value={formData.age}
                onChange={handleChange}
                placeholder="Age"
              />
            </div>

            <div className="input-container">
              <label htmlFor="breed">Breed</label>
              <input
                type="text"
                id="breed"
                value={formData.breed}
                onChange={handleChange}
                placeholder="Breed"
              />
            </div>

            <div className="input-container">
              <label htmlFor="type">Type</label>
              <input
                type="text"
                id="type"
                value={formData.type}
                onChange={handleChange}
                placeholder="Type (e.g., dog, cat)"
              />
            </div>
          </div>

          <div className="column">
            <div className="input-container">
              <label htmlFor="status">Status</label>
              <select id="status" value={formData.status} onChange={handleChange}>
                <option value="">Select Status</option>
                <option value="available">Available</option>
                <option value="adopted">Adopted</option>
              </select>
            </div>

            <div className="input-container">
              <label htmlFor="location">Location</label>
              <input
                type="text"
                id="location"
                value={formData.location}
                onChange={handleChange}
                placeholder="Location"
              />
            </div>

            <div className="input-container">
              <label htmlFor="picture_url">Picture URL</label>
              <input
                type="text"
                id="picture_url"
                value={formData.picture_url}
                onChange={handleChange}
                placeholder="Picture URL"
              />
            </div>
          </div>
        </div>
        <div className="action-buttons">
          <button onClick={handleSave} disabled={loading}>
            {loading ? 'Saving...' : 'Save'}
          </button>
          <button onClick={onBack}>Cancel</button>
          <button
            onClick={handleDelete}
            disabled={loading}
            className="delete-button"
            style={{ backgroundColor: '#d9534f', color: 'white', marginLeft: '10px' }}
          >
            {loading ? 'Deleting...' : 'Delete'}
          </button>
        </div>
      </div>
    </div>
  );
}
