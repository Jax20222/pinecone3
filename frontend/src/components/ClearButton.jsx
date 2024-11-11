import React from 'react';

const ClearButton = ({ handleClearFile }) => (
  <button onClick={handleClearFile} className="clear-button">
    Nuevo archivo
  </button>
);

export default ClearButton;
