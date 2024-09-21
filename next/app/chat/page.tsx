'use client';

import { CSSProperties, useState } from 'react';
import axios from 'axios';

type Message = {
  sender: 'user' | 'ai';
  text: string;
};

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { sender: 'user', text: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setIsLoading(true);

    try {
      // Send the user's message to the Flask backend
      const response = await axios.post<{ text: string }>('api/send-message', {
        message: input,
      });
      console.log(response.data);
      const aiMessage: Message = { sender: 'ai', text: response.data.text };
      setMessages((prevMessages) => [...prevMessages, aiMessage]);
    } catch (error) {
      console.error('Error communicating with the AI model:', error);
      const errorMessage: Message = { sender: 'ai', text: 'Sorry, there was an error.' };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
      setInput('');
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>Chat with Cerebras AI</h1>
      <div style={styles.chatBox}>
        {messages.map((message, index) => (
          <div
            key={index}
            style={{
              ...styles.message,
              alignSelf: message.sender === 'user' ? 'flex-end' : 'flex-start',
              backgroundColor: message.sender === 'user' ? '#daf7a6' : '#f1f1f1',
            }}
          >
            <strong>{message.sender === 'user' ? 'You: ' : 'AI: '}</strong>
            {message.text}
          </div>
        ))}
      </div>
      <div style={styles.inputContainer}>
        <textarea
          value={input}
          onChange={handleInputChange}
          onKeyDown={handleKeyPress}
          placeholder="Type your message..."
          style={styles.input}
          rows={2}
        />
        <button onClick={sendMessage} disabled={isLoading} style={styles.button}>
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  );
}

const styles: { [key: string]: CSSProperties } = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh',
    padding: '0 2rem',
  },
  header: {
    fontSize: '2rem',
    marginBottom: '1rem',
  },
  chatBox: {
    width: '100%',
    maxWidth: '600px',
    minHeight: '400px',
    border: '1px solid #ddd',
    borderRadius: '10px',
    padding: '1rem',
    overflowY: 'auto',
    marginBottom: '1rem',
  },
  message: {
    padding: '0.5rem 1rem',
    borderRadius: '10px',
    margin: '0.5rem 0',
    maxWidth: '80%',
  },
  inputContainer: {
    display: 'flex',
    flexDirection: 'row',
    width: '100%',
    maxWidth: '600px',
  },
  input: {
    flex: 1,
    padding: '0.5rem',
    border: '1px solid #ddd',
    borderRadius: '10px',
    marginRight: '1rem',
  },
  button: {
    padding: '0.5rem 1rem',
    backgroundColor: '#0070f3',
    color: 'white',
    border: 'none',
    borderRadius: '10px',
    cursor: 'pointer',
  },
};