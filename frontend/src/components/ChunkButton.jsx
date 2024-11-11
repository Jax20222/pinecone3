import React from 'react';

const ChunkButton = ({ handleChunking, isActive }) => (
  <button
    onClick={handleChunking}
    className={`chunk-button ${isActive ? 'active' : 'inactive'}`}
    disabled={!isActive}
  >
    Fragmentar Texto
  </button>
);

export default ChunkButton;
