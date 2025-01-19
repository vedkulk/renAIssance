import React, { useState } from 'react';
import roleplays from '../../data/roleplays';
import languages from "../../data/languages";
import SpeechRecognition from './SpeechRecognition';
import TranslatedText from './TranslatedText';
import { FaVolumeUp } from 'react-icons/fa'; // Import the speaker icon

const Roleplay = () => {
  const [selectedRoleplay, setSelectedRoleplay] = useState(roleplays[0].name);
  const [selectedLanguage, setSelectedLanguage] = useState(languages[0].code);
  const [transcript, setTranscript] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [englishResponse, setEnglishResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);

  const handleSpeak = (text) => {
    // If speech is already ongoing, stop it
    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);  // Update the state to indicate speech has stopped
    } else {
      const value = new SpeechSynthesisUtterance(text);
      window.speechSynthesis.speak(value);
      setIsSpeaking(true);  // Update the state to indicate speech is ongoing

      // Optional: Listen for when the speech ends to reset the state
      value.onend = () => {
        setIsSpeaking(false);  // Reset the state when speech ends
      };
    }
  };

  const handleLanguageChange = (event) => {
    setSelectedLanguage(event.target.value);
  };

  const handleRoleplayChange = (event) => {
    setSelectedRoleplay(event.target.value);
  };

  const handleEvaluate = (userTranscript) => {
    setTranscript(userTranscript);
    sendToAPI(userTranscript);
  };

  const sendToAPI = async (userInput) => {
    try {
      setLoading(true);  // Set loading to true before sending the request

      const response = await fetch('http://127.0.0.1:5000/grocery-conversation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_input: userInput,
          preferred_language: selectedLanguage,
        }),
      });

      const data = await response.json();
      console.log('API Response:', data);

      if (data.error) {
        setTranslatedText(`Error: ${data.error}`);
        setEnglishResponse('');  // Clear the English response in case of error
      } else {
        setTranslatedText(data.response);  // Assuming this is the translated response
        setEnglishResponse(data.english_response);  // Assuming the English response is in 'english_response'
      }
    } catch (error) {
      console.error('Error communicating with the API:', error);
      setTranslatedText('An error occurred while communicating with the API.');
      setEnglishResponse('');  // Clear the English response in case of error
    } finally {
      setLoading(false);  // Set loading to false after the request is complete
    }
  };

  return (
    <div className="max-w-full mx-auto px-8 py-8">
      <div className="grid grid-cols-2 gap-6">
        {/* Roleplay Selection */}
        <div>
          <label htmlFor="roleplay-select" className="text-2xl block font-medium text-gray-700">
            Select Roleplay:
          </label>
          <select
            id="roleplay-select"
            value={selectedRoleplay}
            onChange={handleRoleplayChange}
            className="mt-2 p-2 rounded-md border border-gray-300 w-full"
          >
            {roleplays.map((roleplay, index) => (
              <option key={index} value={roleplay.name}>
                {roleplay.name}
              </option>
            ))}
          </select>
        </div>

        {/* Language Selection */}
        <div>
          <label htmlFor="language-select" className="text-2xl block font-medium text-gray-700">
            Select Target Language:
          </label>
          <select
            id="language-select"
            value={selectedLanguage}
            onChange={handleLanguageChange}
            className="mt-2 p-2 rounded-md border border-gray-300 w-full"
          >
            {languages.map((lang) => (
              <option key={lang.code} value={lang.code}>
                {lang.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="mt-10 grid grid-cols-2 gap-8">
      <SpeechRecognition onEvaluate={handleEvaluate} />

      <div className="bg-white rounded-xl shadow-md p-8 h-[600px]">
      {/* Loading Indicator */}
      {loading && <div className="mt-4 text-center">Loading...</div>}

      <div className="flex justify-between items-center">
        <div>
          <div className="text-2xl font-semibold">Translated Text:</div>
          {translatedText && !loading && (
            <div>
              <FaVolumeUp
                onClick={() => handleSpeak(translatedText)} // Pass translated text to speech function
                size={24}
                className="cursor-pointer text-blue-500 hover:text-blue-700"
              />
              <div>{translatedText}</div>
            </div>
          )}
        </div>
      </div>
      {englishResponse && !loading && (
        <div>
          <div className="text-2xl font-semibold mt-10">English Response:</div>
          <FaVolumeUp
            onClick={() => handleSpeak(englishResponse)}  // Pass English response to speech function
            size={24}
            className="cursor-pointer text-blue-500 hover:text-blue-700"
          />
          <div>{englishResponse}</div>
        </div>
      )}
    </div>
    </div>
      
      
    </div>
  );
};

export default Roleplay;
