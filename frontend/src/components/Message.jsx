import React from 'react';

const Message = ({ message }) => message && <p className="message">{message}</p>;

export default Message;
