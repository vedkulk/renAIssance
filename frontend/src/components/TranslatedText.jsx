import React from 'react';

const TranslatedText = ({ translatedText }) => (
  <div className="bg-white rounded-xl shadow-md p-8 h-[600px]">
    <h2 className="text-2xl font-bold text-gray-800">Translated Text</h2>
    <p className="text-lg text-gray-600 mt-4">{translatedText}</p>
  </div>
);

export default TranslatedText;
