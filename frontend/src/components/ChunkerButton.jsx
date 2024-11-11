// src/components/ChunkerButton.jsx
import React from 'react';

const ChunkerButton = ({ onClick }) => {
  return (
    <button onClick={onClick} style={{ marginTop: '20px', padding: '10px 20px' }}>
      Realizar chunking
    </button>
  );
};

export default ChunkerButton;
