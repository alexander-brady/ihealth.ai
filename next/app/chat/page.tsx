'use client';  // This tells Next.js it's a Client Component

import { useState, useCallback } from 'react';
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
  const [isSending, setIsSending] = useState<boolean>(false); // Track message sending

  const sendMessage = useCallback(async () => {
    if (!input.trim() || isSending) return; // prevent re-sending if already sending
    setIsSending(true); // prevent multiple sends
    const userMessage: Message = { sender: 'user', text: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

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
      setInput(''); // Reset input after sending
      setIsSending(false); // Allow another message to be sent
    }
  }, [input, isSending]);

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
      />
    </div>
  );
}
