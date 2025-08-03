import React, { useState, useRef } from 'react';
import html2canvas from 'html2canvas';
import ImageUploader from './components/ImageUploader';
import BlindOverlay from './components/BlindOverlay';
import logo from './assets/exceptional-logo.png';
import './App.css';

const App = () => {
  const [image, setImage] = useState(null);
  const [color, setColor] = useState('#888');
  const [blindType, setBlindType] = useState('roller');
  const captureRef = useRef(null);

  const handleDownload = async () => {
    if (!captureRef.current) return;

    try {
      const canvas = await html2canvas(captureRef.current);
      const link = document.createElement('a');
      link.download = 'blind-visualizer.png';
      link.href = canvas.toDataURL('image/png');
      link.click();
    } catch (error) {
      console.error('Download failed:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center px-4 py-12 space-y-12 text-center">
      {/* Logo */}
      <img src={logo} alt="Exceptional Blinds company logo" className="w-28" />

      {/* Title */}
      <h1 className="text-4xl font-bold">Blind Visualizer</h1>

      {/* Image Upload */}
      <div className="w-full max-w-md mx-auto">
        <ImageUploader onImageLoad={setImage} />
      </div>

      {/* Controls */}
      <div className="w-full max-w-md mx-auto grid grid-cols-1 sm:grid-cols-2 gap-6">
        <div className="flex flex-col items-center text-center">
          <label className="mb-2 font-medium">Color</label>
          <input
            type="color"
            value={color}
            onChange={(e) => setColor(e.target.value)}
            className="border rounded h-10 w-20"
          />
        </div>

        <div className="flex flex-col items-center text-center">
          <label className="mb-2 font-medium">Type</label>
          <select
            value={blindType}
            onChange={(e) => setBlindType(e.target.value)}
            className="px-2 py-2 border rounded w-40"
          >
            <option value="roller">Roller</option>
            <option value="roman">Roman</option>
            <option value="venetian">Venetian</option>
            <option value="vertical">Vertical</option>
          </select>
        </div>
      </div>

      {/* Visualizer */}
      <div className="w-full max-w-3xl mx-auto">
        <div ref={captureRef} className="relative">
          <BlindOverlay imgSrc={image} blindType={blindType} color={color} />
        </div>
      </div>

      {/* Buttons */}
<div className="w-full max-w-md mx-auto flex flex-col sm:flex-row justify-center items-center gap-4 mt-8">
  <div className="w-full sm:w-auto">
    <button
      onClick={handleDownload}
      className="w-full sm:w-auto px-6 py-3 bg-green-600 text-white rounded hover:bg-green-700"
    >
      Download Styled Image
    </button>
  </div>

  {image && (
    <div className="w-full sm:w-auto">
      <a href={image} download="original-room.png">
        <button className="w-full sm:w-auto px-6 py-3 bg-blue-600 text-white rounded hover:bg-blue-700">
          Download Original Image
        </button>
      </a>
    </div>
  )}
</div>
    </div>
  );
};

export default App;
