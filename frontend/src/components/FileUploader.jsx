// src/components/FileUploader.jsx
import React, { useState } from 'react';

const FileUploader = ({ setMessage }) => {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!selectedFile) {
      setMessage('Por favor, selecciona un archivo PDF.');
      return;
    }

    const formData = new FormData();
    formData.append('pdf', selectedFile);

    try {
      const response = await fetch('http://127.0.0.1:5000/convert_pdf', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        setMessage('Archivo convertido y guardado exitosamente.');
      } else {
        setMessage('Hubo un error al subir el archivo.');
      }
    } catch (error) {
      setMessage('Error: No se pudo completar la solicitud.');
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginTop: '20px', textAlign: 'center' }}>
      <input
        type="file"
        accept="application/pdf"
        onChange={handleFileChange}
        style={{ marginBottom: '20px', padding: '5px' }}
      />
      <button type="submit" style={{ padding: '10px 20px' }}>Subir y convertir</button>
    </form>
  );
};

export default FileUploader;
