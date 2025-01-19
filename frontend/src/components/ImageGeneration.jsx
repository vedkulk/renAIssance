import React, { useState } from 'react';
import axios from 'axios';
import words from '../../data/words';

const ImageGeneration = () => {
  const [scenario, setScenario] = useState('');
  const [language, setLanguage] = useState('en');
  const [image, setImage] = useState(null);

  const handleScenarioChange = (e) => {
    setScenario(e.target.value);
  };

  const handleLanguageChange = (e) => {
    setLanguage(e.target.value);
  };

  const handleGenerateImage = async () => {
    if (!scenario) {
      alert('Please select a scenario');
      return;
    }
  
    console.log('Sending data:', { scenario, language });
  
    try {
      const response = await axios.post('http://127.0.0.1:5000/generate-image', {
        scenario,
        language
      });
      setImage(response.data.image_url); // Assuming API returns image_url
    } catch (error) {
      console.error('Error generating image:', error);
      alert('Error generating image.');
    }
  };
  

  const scenarios = Object.keys(words);

  return (
    <div>
      <h2>Generate Image</h2>

      <div>
        <label>Scenario: </label>
        <select onChange={handleScenarioChange}>
          <option value="">Select a scenario</option>
          {scenarios.map((scenario, index) => (
            <option key={index} value={scenario}>
              {scenario}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label>Language: </label>
        <select onChange={handleLanguageChange} value={language}>
          <option value="en">English</option>
          <option value="es">Spanish</option>
          <option value="fr">French</option>
          {/* Add other languages if needed */}
        </select>
      </div>

      <button onClick={handleGenerateImage}>Generate Image</button>

      {image && (
        <div>
          <h3>Generated Image:</h3>
          <img src={image} alt="Generated" style={{ maxWidth: '100%', height: 'auto' }} />
        </div>
      )}
    </div>
  );
};

export default ImageGeneration;
