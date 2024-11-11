// src/components/MessageDisplay.jsx
import React from 'react';

const MessageDisplay = ({ message }) => {
  return message ? <p style={{ marginTop: '20px', textAlign: 'center' }}>{message}</p> : null;
};

export default MessageDisplay;
