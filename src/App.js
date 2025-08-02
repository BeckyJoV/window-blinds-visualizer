import React from 'react';
import exceptionalLogo from './assets/exceptional-logo.png';
import './App.css';

function App() {
  return (
    <div className="App text-center p-6">
      {/* Logo */}
      <img
        src={exceptionalLogo}
        alt="Exceptional Blinds Logo"
        className="w-24 mx-auto mb-4"
      />

      {/* Heading and intro */}
      <h1 className="text-3xl font-bold mb-2">Exceptional Blinds Visualizer Test App</h1>
      <p className="text-gray-700">Welcome to the prototype!</p>
    </div>
  );
}

export default App;
