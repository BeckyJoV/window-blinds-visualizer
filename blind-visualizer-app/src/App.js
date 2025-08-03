import React from 'react';
import exceptionalLogo from './assets/exceptional-logo.png';
import './App.css';

function App() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-white p-6">
      <img src={exceptionalLogo} alt="Logo" className="h-32 mb-6" />
      <h1 className="text-5xl font-extrabold mb-4">Exceptional Blinds Visualizer</h1>
      <p className="text-xl text-gray-700">Upload a photo of your room and preview different blind styles.</p>
    </div>
  );
}

export default App;

