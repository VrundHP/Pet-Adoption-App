import React, { useState } from 'react';
import './AddPet.css';

interface AddPetProps {
  onBack: () => void;
}

const AddPet: React.FC<AddPetProps> = ({ onBack }) => {
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    description: 'No description provided.',
    breed: '',
    picture_url: '',
    status: 'available',
    type: '',
    location: '',
  });

  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:5000';

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${backendUrl}/pets`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...formData, admin_id: 1 }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.message || 'Failed to add pet.');
      }

      alert('Pet added successfully!');
      onBack();
    } catch (err) {
      console.error('Error adding pet:', err);
      setError('Failed to add pet. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="add-pet-wrapper">
      <div className="add-pet-box">
        <h2 className="thick">Add a New Pet</h2>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <input name="name" value={formData.name} onChange={handleChange} placeholder="Name" required />
            <input name="age" value={formData.age} onChange={handleChange} placeholder="Age" required />
            <input name="breed" value={formData.breed} onChange={handleChange} placeholder="Breed" required />
            <input
              name="picture_url"
              value={formData.picture_url}
              onChange={handleChange}
              placeholder="Picture URL"
              required
            />
            <select name="status" value={formData.status} onChange={handleChange}>
              <option value="available">Available</option>
              <option value="adopted">Adopted</option>
            </select>
            <input name="type" value={formData.type} onChange={handleChange} placeholder="Type (Dog, Cat...)" required />
            <input name="location" value={formData.location} onChange={handleChange} placeholder="Location" required />
          </div>

          {error && <p className="error">{error}</p>}
          <br></br>
          <button type="submit" disabled={loading}>
            {loading ? 'Adding...' : 'Add Pet'}
          </button>
        </form>
        <button className="back-button" onClick={onBack}>
          Back
        </button>
      </div>
    </div>
  );
};

export default AddPet;
