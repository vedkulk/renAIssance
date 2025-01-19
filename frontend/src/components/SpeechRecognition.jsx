import React, { useState, useEffect } from 'react';

const SpeechRecognition = ({ onEvaluate }) => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [recognition, setRecognition] = useState(null);

  useEffect(() => {
    if (typeof window !== 'undefined' && 'webkitSpeechRecognition' in window) {
      const recognition = new window.webkitSpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;

      recognition.onstart = () => {
        setIsListening(true);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognition.onresult = (event) => {
        let currentTranscript = '';
        for (let i = 0; i < event.results.length; i++) {
          currentTranscript += event.results[i][0].transcript;
        }
        setTranscript(currentTranscript);
      };

      recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
      };

      setRecognition(recognition);
    }
  }, []);

  const startListening = () => {
    if (recognition) {
      recognition.start();
    }
  };

  const stopListening = () => {
    if (recognition) {
      recognition.stop();
    }
  };

  const handleEvaluate = () => {
    onEvaluate(transcript);
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-8 h-[600px]">
      <div className="space-y-4 h-full flex flex-col">
        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-bold text-gray-800">Speech Recognition</h2>
          <div className="flex space-x-2">
            <button
              onClick={startListening}
              disabled={isListening}
              className={`px-4 py-2 rounded-md ${
                isListening
                  ? 'bg-gray-300 cursor-not-allowed'
                  : 'bg-blue-500 hover:bg-blue-600 text-white'
              }`}
            >
              Start
            </button>
            <button
              onClick={stopListening}
              disabled={!isListening}
              className={`px-4 py-2 rounded-md ${
                !isListening
                  ? 'bg-gray-300 cursor-not-allowed'
                  : 'bg-red-500 hover:bg-red-600 text-white'
              }`}
            >
              Stop
            </button>
          </div>
        </div>
        
        <div className="mt-4">
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${
              isListening ? 'bg-green-500' : 'bg-gray-300'
            }`}></div>
            <span className="text-lg text-gray-600">
              {isListening ? 'Listening...' : 'Not listening'}
            </span>
          </div>
        </div>

        <div className="flex-1 flex flex-col">
          <h3 className="text-lg font-semibold text-gray-700">Transcript:</h3>
          <div className="mt-2 p-4 bg-gray-50 rounded-md flex-1 overflow-y-auto ">
            {transcript || <div className='text-gray-400 text-xl'>Hello I want to learn how to speak .....</div>}
          </div>
        </div>
        
        <button
          onClick={handleEvaluate}
          className='px-4 py-2 rounded-md text-xl bg-blue-400 hover:bg-blue-600 text-white'
        >
          Evaluate
        </button>
      </div>
    </div>
  );
};

export default SpeechRecognition;
