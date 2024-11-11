import React from 'react';

const FileInput = ({ fileInputRef, handleFileChange }) => (
  <input
    ref={fileInputRef}
    type="file"
    accept="application/pdf"
    onChange={handleFileChange}
    className="file-input"
  />
);

export default FileInput;
