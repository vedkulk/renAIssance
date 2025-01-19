import React, { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header.jsx';
import SpeechRecognition from './components/SpeechRecognition.jsx';
import TranslatedText from './components/TranslatedText.jsx';
import StoryMode from './components/StoryMode.jsx';
import Roleplay from './components/Roleplay.jsx';
import ImageGeneration from './components/ImageGeneration.jsx';
import MainContent from './components/MainContent.jsx';

const App = () => {  
  return (
    <BrowserRouter>
      <div>
        <Header />
        <Routes>
          <Route path="/" element={<MainContent />} />
          <Route path="/story-mode" element={<StoryMode />} />
          <Route path="/roleplay" element={<Roleplay />} />
          <Route path="/image-generation" element={<ImageGeneration />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
};

export default App