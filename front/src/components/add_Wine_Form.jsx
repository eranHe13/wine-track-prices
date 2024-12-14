import React, { useState, useEffect } from 'react';
import { addWine, get_user_wines } from "../server";

const AddProductForm = ({ user, updateUser }) => {
  const [wineNames, setWineNames] = useState([]);
  const [selectedName, setSelectedName] = useState('');
  const [desiredPrice, setDesiredPrice] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    // Fetch wine names from the CSV file
    fetch('/wine_names.csv')
      .then(response => response.text())
      .then(text => {
        // Split the CSV text into an array of wine names
        const names = text.split('\n').map(name => name.trim());
        setWineNames(names.filter(name => name)); // Filter out empty lines
      })
      .catch(error => {
        console.error('Error fetching wine names:', error);
      });
  }, []);

  const handleNameChange = (event) => {
    setSelectedName(event.target.value);
  };

  const handlePriceChange = (event) => {
    setDesiredPrice(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(''); // Clear any existing error messages

    if (!selectedName) {
      setError('Please select or enter a wine name.');
      return;
    } else if (!desiredPrice || isNaN(desiredPrice) || parseFloat(desiredPrice) <= 0) {
      setError('Please enter a valid positive price.');
      return;
    }

    try {
      await addWine({ "user_id": user.id, "wine_name": selectedName, "price": desiredPrice }, updateUser);
      get_user_wines(user.id, updateUser);
    } catch (error) {
      setError('An error occurred while saving the product.');
    }
  };

  return (
<div style={{ display: 'flex',  alignItems: 'center'  , direction:"rtl"}}>
    <form onSubmit={handleSubmit}>
      {error && <div style={{ color: 'red', paddingBottom: '10px'  }}>{error}</div>}
      <div style={{alignSelf:"flex-end", paddingBottom: "10px", width: "350px" }}>
        <label className="form-label" style={{ fontSize: "20px" }}>שם היין</label>
        <input
          className="form-control"
          list="wineNames"
          value={selectedName}
          onChange={handleNameChange}
        />
        <datalist id="wineNames">
          {wineNames.map((name, index) => (
            <option key={index} value={name} />
          ))}
        </datalist>
      </div>
      <div style={{alignSelf:"center" ,  paddingBottom: "10px", width: "150px"  , textAlign: 'right'}}>
        <label className="form-label" style={{ fontSize: "20px" }}>מחיר מבוקש</label>
        <input
          className="form-control"
          type="text"
          value={desiredPrice}
          onChange={handlePriceChange}
        />
      </div>
      <button className="btn btn-primary" type="submit">Save Product</button>
    </form>
    </div>
  );
};

export default AddProductForm;
