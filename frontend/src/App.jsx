import React, { useState, useRef } from 'react';
import './App.css';
import FileInput from './components/FileInput';
import SubmitButton from './components/SubmitButton';
import ClearButton from './components/ClearButton';
import ChunkButton from './components/ChunkButton';
import Message from './components/Message';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState('');
  const [isChunkButtonActive, setIsChunkButtonActive] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setIsChunkButtonActive(false);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!selectedFile) {
      setMessage('Por favor, selecciona un archivo PDF.');
      return;
    }

    setIsLoading(true);
    setMessage('');

    const formData = new FormData();
    formData.append('pdf', selectedFile);

    try {
      const response = await fetch('http://127.0.0.1:5000/convert_pdf', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        setMessage('Archivo convertido y guardado exitosamente.');
        setIsChunkButtonActive(true);
      } else {
        setMessage('Hubo un error al convertir el archivo.');
      }
    } catch (error) {
      setMessage('Error: No se pudo completar la solicitud.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleChunking = async () => {
    if (!selectedFile) {
      setMessage('Por favor, convierte el PDF primero.');
      return;
    }

    setIsLoading(true);
    setMessage('');

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
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearFile = () => {
    setSelectedFile(null);
    setMessage('Archivo limpiado. Puedes seleccionar uno nuevo.');
    setIsChunkButtonActive(false);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="App">
      <h1>Procesador de PDF</h1>
      <form onSubmit={handleSubmit} className="form-container">
        <FileInput fileInputRef={fileInputRef} handleFileChange={handleFileChange} />
        <div className="button-group">
          <SubmitButton handleSubmit={handleSubmit} />
          <ClearButton handleClearFile={handleClearFile} />
        </div>
      </form>
      <ChunkButton handleChunking={handleChunking} isActive={isChunkButtonActive} />
      <Message message={isLoading ? 'Procesando...' : message} />
    </div>
  );
}

export default App;
