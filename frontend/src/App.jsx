import React from 'react'
import Header from './components/Header.jsx'
import SpeechRecognition from './components/SpeechRecognition.jsx'
const App = () => {
  return (
    <>
      <div>
        <Header/>
        <main className="max-w-full mx-auto px-8 py-8">
        <div className="grid grid-cols-2 gap-8">
              <SpeechRecognition />          
          <div className="bg-white rounded-xl shadow-md p-8 h-[600px]">
            <h2 className="text-2xl font-bold text-gray-800">Additional Content</h2>
            <p className="text-lg text-gray-600 mt-4">This space is available for additional features or content.</p>
          </div>
        </div>
      </main>
      </div>
    </>
  )
}

export default App