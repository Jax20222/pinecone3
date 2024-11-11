import React, { useState } from 'react';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState('');

  // Manejar la selección del archivo
  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  // Función para enviar el archivo PDF y convertirlo a texto
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
        setMessage('Hubo un error al convertir el archivo.');
      }
    } catch (error) {
      setMessage('Error: No se pudo completar la solicitud.');
    }
  };

  // Función para realizar el chunking del texto
  const handleChunking = async () => {
    if (!selectedFile) {
      setMessage('Por favor, convierte el PDF primero.');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/chunk_text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          file_name: selectedFile.name,
        }),
      });

      if (response.ok) {
        setMessage('Texto fragmentado exitosamente.');
      } else {
        setMessage('Hubo un error al fragmentar el texto.');
      }
    } catch (error) {
      setMessage('Error: No se pudo completar la solicitud.');
    }
  };

  return (
    <div className="App">
      <h1>Procesador de PDF</h1>
      <form onSubmit={handleSubmit} className="form-container">
        <input
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
          className="file-input"
        />
        <button type="submit" className="submit-button">
          Subir y convertir
        </button>
      </form>
      <button onClick={handleChunking} className="chunk-button">
        Fragmentar Texto
      </button>
      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default App;
