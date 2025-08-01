import React from "react";
import ImageUploader from "./components/ImageUploader";
import BlindSelector from "./components/BlindSelector";
import BlindOverlay from "./components/BlindOverlay";
import ExportButton from "./components/ExportButton";
import { useBlindsStore } from "./store/blindsStore";

export default function App() {
  const uploadedImage = useBlindsStore((s) => s.uploadedImage);

  return (
    <div className="min-h-screen p-4 bg-gray-100">
      <h1 className="text-3xl font-bold mb-4">Window Blinds Visualizer</h1>
      <ImageUploader />
      {uploadedImage && (
        <div className="relative mt-6">
          <BlindOverlay />
        </div>
      )}
      <div className="mt-6 flex gap-4">
        <BlindSelector />
        <ExportButton />
      </div>
    </div>
  );
}