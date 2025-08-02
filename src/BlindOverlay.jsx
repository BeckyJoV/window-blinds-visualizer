import React from 'react';
import Draggable from 'react-draggable';

const BlindOverlay = ({ imgSrc, blindType, color, detections = [] }) => {
  if (!imgSrc) return null;

  return (
    <div className="relative w-full max-w-3xl mx-auto mt-6">
      {/* Room image */}
      <img src={imgSrc} alt="Room" className="w-full rounded-lg" />

      {/* AI-detected window overlays */}
      {detections.length > 0 &&
        detections.map((box, i) => (
          <div
            key={i}
            className="absolute border-2 border-blue-500"
            style={{
              left: box.x,
              top: box.y,
              width: box.w,
              height: box.h,
            }}
          >
            {/* Optional: blind preview inside box */}
            <div
              className="w-full h-full"
              style={{
                backgroundColor: color,
                mixBlendMode: 'multiply',
                opacity: 0.6,
              }}
            />
          </div>
        ))}

      {/* Manual draggable blind */}
      {detections.length === 0 && (
        <Draggable bounds="parent">
          <div
            className="absolute w-[150px] h-[100px] opacity-80 cursor-move"
            style={{
              backgroundColor: color,
              mixBlendMode: 'multiply',
            }}
          />
        </Draggable>
      )}
    </div>
  );
};

export default BlindOverlay;
