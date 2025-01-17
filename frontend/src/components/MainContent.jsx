import React, { useState } from 'react';
import languages from "../../data/languages";
import SpeechRecognition from "./SpeechRecognition";
import TranslatedText from "./TranslatedText";

const MainContent = () => {
    const [selectedLanguage, setSelectedLanguage] = useState(languages[0].code);
    const [translatedText, setTranslatedText] = useState('');

    const handleLanguageChange = (event) => {
        setSelectedLanguage(event.target.value);
    };
      const handleEvaluate = async (inputText) => {
        try {
          const response = await fetch('http://127.0.0.1:5000/translate', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              input_text: inputText,
              target_language: selectedLanguage,
            }),
          });
      
          if (response.ok) {
            const data = await response.json();
            setTranslatedText(data.translated_text);
          } else {
            console.error('Translation failed:', response.statusText);
          }
        } catch (error) {
          console.error('Error:', error);
        }
      };
    return(
    <main className="max-w-full mx-auto px-8 py-8">
      <div className="mt-4">
        <label htmlFor="language-select" className="text-2xl block font-medium text-gray-700">
          Select Target Language:
        </label>
        <select
          id="language-select"
          value={selectedLanguage}
          onChange={handleLanguageChange}
          className="mt-2 p-2 rounded-md border border-gray-300"
        >
          {languages.map((lang) => (
            <option key={lang.code} value={lang.code}>
              {lang.name}
            </option>
          ))}
        </select>
      </div>
      <div className="mt-10 grid grid-cols-2 gap-8">
        <SpeechRecognition onEvaluate={handleEvaluate} />
        <TranslatedText translatedText={translatedText} />
      </div>
    </main>
    )
};

export default MainContent
