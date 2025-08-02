const handleImageUpload = async (file) => {
  const formData = new FormData();
  formData.append('image', file);

  const res = await fetch('/api/detect-windows', {
    method: 'POST',
    body: formData,
  });

  const data = await res.json();
  setDetections(data); // Store window bounding boxes
};
