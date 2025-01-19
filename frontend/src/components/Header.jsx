import React from 'react';

const Header = () => {
  return (
    <header className="bg-white shadow-md">
      <div className="max-w-7xl mx-3 px-4 py-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">
            <a href='/'>
          Speech Recognition App
            </a>
          </h1>
          <nav className="ml-8">
            <ul className="flex items-center gap-8">
              <li>
                <a href="/story-mode" className="text-lg font-medium text-blue-500 hover:text-blue-900">Story Mode</a>
              </li>
              <li>
                <a href="/roleplay" className="text-lg font-medium text-blue-500 hover:text-blue-900">Roleplay</a>
              </li>
              <li>
                <a href="/image-generation" className="text-lg font-medium text-blue-500 hover:text-blue-900">Image Generation</a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;