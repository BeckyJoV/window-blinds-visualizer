import React, { useRef, useState } from 'react';

const ImageUploader = ({ onImageLoad }) => {
const inputRef = useRef();
const [preview, setPreview] = useState(null);

const handleFile = (e) => {
const file = e.target.files[0];
if (!file) return;
const reader = new FileReader();
reader.onload = () => {
setPreview(reader.result);
onImageLoad(reader.result);
};
reader.readAsDataURL(file);
};

return (
<div className="my-4">
<input
type="file"
accept="image/*"
ref={inputRef}
className="hidden"
onChange={handleFile}
/>
<button
onClick={() => inputRef.current.click()}
className="px-4 py-2 bg-blue-600 text-white rounded"
>
Upload Room Image
</button>
{preview && (
<img src={preview} alt="Preview" className="mt-4 max-w-full rounded shadow" />
)}
</div>
);
};

export default ImageUploader;