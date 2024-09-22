'use client';

import { useState } from 'react';
import axios from 'axios';
import ChatBubble from '../components/chatBotComps/chatBubble';
import InputArea from '../components/chatBotComps/input';

export type Message = {
  sender: 'user' | 'ai';
  text: string;
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>('');
  const [disabled, setDisabled] = useState<boolean>(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { sender: 'user', text: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput('');
    setDisabled(true);
      

    try {
      // Send the user's message to the Flask backend
      const response = await axios.post<{ text: string }>('flask/send-message', {
        message: input,
      });
      const aiMessage: Message = { sender: 'ai', text: response.data.text };
      setMessages((prevMessages) => [...prevMessages, aiMessage]);
    } catch (error) {
      console.error('Error communicating with the AI model:', error);
      setMessages((prevMessages) => [...prevMessages, { sender: 'ai', text: 'Sorry, there was an error.' }]);
    } finally {
      setDisabled(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8">
      <h1 className="text-center text-3xl font-bold mb-4">Chat with iHealth.<span className="text-blue-800">ai</span></h1>
      <div className="w-full max-w-screen-lg h-[550px] bg-slate-100 rounded-lg p-4 overflow-y-auto mb-4">
        {messages.map((message, index) => (
          <ChatBubble key={index} message={message} />
        ))}
      </div>
      <InputArea
        input={input}
        setInput={setInput}
        sendMessage={sendMessage}
        disabled={disabled}
      />
    </div>
  );
}