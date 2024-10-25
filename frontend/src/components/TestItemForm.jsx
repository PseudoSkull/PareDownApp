// ./components/TestItemForm
import React, { useState } from 'react';
import axios from 'axios';

const DataForm = () => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Create the payload data to be sent to the backend
    const data = {
      action: "AddTestItem",
      name: name,
      description: description
    };

    try {
      const response = await axios.post('http://localhost:5000/actionendpoint', data, {
        headers: {
            'Content-Type': 'application/json'
        }
      });

      // Alert success message if the submission was successful
      alert(response.data.message);
      setName('');
      setDescription('');
    } catch (error) {
      console.error("Error submitting data:", error);
      alert("Error submitting data. Please try again.");
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Name:
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </label>
        <br />
        <label>
          Description:
          <input
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </label>
        <br />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default DataForm;
