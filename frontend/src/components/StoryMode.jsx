import React, { useState } from "react";
import { FaVolumeUp } from 'react-icons/fa'; // Import the speaker icon

const StoryMode = () => {
  const [language, setLanguage] = useState(""); // User input for language
  const [difficulty, setDifficulty] = useState(""); // User input for difficulty
  const [story, setStory] = useState(""); // API response

  const [isSpeaking, setIsSpeaking]= useState(false); // Track whether speech synthesis is currently active

const handleSpeak = () => {
  // If speech is already ongoing, stop it
  if (isSpeaking) {
    window.speechSynthesis.cancel();
    setIsSpeaking(false);  // Update the state to indicate speech has stopped
  } else {
    const value = new SpeechSynthesisUtterance(story);
    window.speechSynthesis.speak(value);
    setIsSpeaking(true)  // Update the state to indicate speech is ongoing

    // Optional: Listen for when the speech ends to reset the state
    value.onend = () => {
      setIsSpeaking(false);  // Reset the state when speech ends
    };
  }
};
const generateStory = async () => {
  try {
    const response = await fetch("http://127.0.0.1:5000/generate-story", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        language: language,
        difficulty: difficulty,
      }),
      credentials: "include",  // Include credentials (cookies) in the request
    });

    if (!response.ok) {
      throw new Error("Failed to fetch story");
    }

    const data = await response.json();
    setStory(data.story || data.error);
  } catch (error) {
    console.error("Error generating story:", error);
    setStory("An error occurred while generating the story.");
  }
};



  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      
      
      <div style={{ marginBottom: "1rem" }}>
        <label>
          <strong className="text-2xl">Language:</strong>
          <input
            type="text"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            placeholder="Enter language"
            style={{ marginLeft: "1rem", padding: "0.5rem" }}
          />
        </label>
      </div>
      <div style={{ marginBottom: "1rem" }}>
        <label>
          <strong className="text-2xl">Difficulty:</strong>
          <select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
            style={{ marginLeft: "1rem", padding: "0.5rem" }}
          >
            <option value="">Select difficulty</option>
            <option value="Easy">Easy</option>
            <option value="Moderate">Moderate</option>
            <option value="High">High</option>
          </select>
        </label>
      </div >
      <button 
        onClick={generateStory}
        style={{
          padding: "0.5rem 1rem",
          backgroundColor: "#007BFF",
          color: "#FFF",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
      >
        Generate Story 
      </button>
      <div style={{ marginTop: "2rem" }}>
      <div className="flex items-center space-x-2  mb-5">
        <h1 className="text-2xl">Generated Story:</h1>
        <FaVolumeUp
          onClick={handleSpeak}
          size={24}
          className="cursor-pointer text-blue-500 hover:text-blue-700"
        />
      </div>
      <p
        style={{
          whiteSpace: "pre-wrap",
          backgroundColor: "#F9F9F9",
          padding: "1rem",
          borderRadius: "5px",
          color: "black", // Change text color to black
        }}
      >
        {story || "No story generated yet."}
      </p>
      </div>
    </div>
  );
};


export default StoryMode