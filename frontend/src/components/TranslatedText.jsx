import React from 'react';
import { FaVolumeUp } from 'react-icons/fa'; // Import the speaker icon

const TranslatedText = ({ translatedText }) => {
  const handleSpeak = () => {
    const value = new SpeechSynthesisUtterance(translatedText);
    window.speechSynthesis.speak(value);
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-8 h-[600px]">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-800">Translated Text</h2>
        <FaVolumeUp
          onClick={handleSpeak}
          size={24}
          className="cursor-pointer text-blue-500 hover:text-blue-700"
        />
      </div>
      <p className="text-lg text-gray-600 mt-4">{translatedText}</p>
    </div>
  );
};

export default TranslatedText;
