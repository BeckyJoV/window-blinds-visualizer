import React, { useState, useRef } from 'react';
import html2canvas from 'html2canvas';
import ImageUploader from './components/ImageUploader';
import BlindOverlay from './components/BlindOverlay';
import {
  FacebookShareButton,
  TwitterShareButton,
  WhatsappShareButton,
  FacebookIcon,
  TwitterIcon,
  WhatsappIcon
} from 'react-share';

const App = () => {
  const [image, setImage] = useState(null);
  const [color, setColor] = useState('#888');
  const [blindType, setBlindType] = useState('roller');
  const [shareUrl, setShareUrl] = useState('');
  const captureRef = useRef(null);

  const handleDownload = async () => {
    if (!captureRef.current) return;

    try {
      const canvas = await html2canvas(captureRef.current);
      const dataUrl = canvas.toDataURL('image/png');

      // Create download link
      const link = document.createElement('a');
      link.download = 'blind-visualizer.png';
      link.href = dataUrl;
      link.click();

      // Optionally set share URL (e.g. upload to server or use data URL)
      setShareUrl(dataUrl); // For demo purposes, using data URL
    } catch (error) {
      console.error('Download failed:', error);
    }
  };

  return (
    <div className="p-6 bg-gray-50 min-h-screen text-center">
      {/* Logo */}
      <img
        src="/exceptional-logo.png"
        alt="Exceptional Blinds company logo"
        className="w-24 mx-auto mb-4"
      />

      <h1 className="text-3xl font-bold mb-4">Blind Visualizer</h1>
      <ImageUploader onImageLoad={setImage} />

      {/* Controls */}
      <div className="mt-4 flex justify-center items-center gap-4">
        <label className="flex items-center gap-2">
          Color:
          <input
            type="color"
            value={color}
            onChange={(e) => setColor(e.target.value)}
            className="border rounded"
          />
        </label>

        <label className="flex items-center gap-2">
          Type:
          <select
            value={blindType}
            onChange={(e) => setBlindType(e.target.value)}
            className="px-2 py-1 border rounded"
          >
            <option value="roller">Roller</option>
            <option value="roman">Roman</option>
            <option value="venetian">Venetian</option>
            <option value="vertical">Vertical</option>
          </select>
        </label>
      </div>

      {/* Visual container */}
      <div ref={captureRef} className="relative mt-6 inline-block">
        <BlindOverlay imgSrc={image} blindType={blindType} color={color} />
      </div>

      {/* Download buttons */}
      <div className="mt-6 flex justify-center gap-4 flex-wrap">
        <button
          onClick={handleDownload}
          className="px-4 py-2 bg-green-600 text-white rounded"
        >
          Download Styled Image
        </button>

        {image && (
          <a href={image} download="customized-room.png">
            <button className="px-4 py-2 bg-blue-600 text-white rounded">
              Download Original Image
            </button>
          </a>
        )}
      </div>

      {/* Social Share Buttons */}
      {shareUrl && (
        <div className="mt-6 flex justify-center gap-4">
          <FacebookShareButton url={shareUrl}>
            <FacebookIcon size={32} round />
          </FacebookShareButton>
          <TwitterShareButton url={shareUrl}>
            <TwitterIcon size={32} round />
          </TwitterShareButton>
          <WhatsappShareButton url={shareUrl}>
            <WhatsappIcon size={32} round />
          </WhatsappShareButton>
        </div>
      )}
    </div>
  );
};

export default App;
