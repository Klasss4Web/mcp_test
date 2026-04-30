import React, { useState, useRef, useEffect } from 'react';
import '../styles/modern.css';
import { API_BASE_URL } from '../apiBase';

interface Message {
  sender: 'user' | 'bot';
  text: string;
}

const ChatWidget: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { sender: 'bot', text: 'Hi! I am your AI assistant. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    const userText = input.trim();
    if (!userText) return;
    setMessages(msgs => [...msgs, { sender: 'user', text: userText }]);
    setInput('');
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/chat/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: 'guest', message: userText })
      });
      const data = await res.json();
      setMessages(msgs => [...msgs, { sender: 'bot', text: data.response || 'Sorry, I did not understand that.' }]);
    } catch (err) {
      setMessages(msgs => [...msgs, { sender: 'bot', text: 'Sorry, there was a problem connecting to the server.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-widget">
      <div className="chat-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`chat-msg chat-msg-${msg.sender}`}>{msg.text}</div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <form className="chat-input-row" onSubmit={sendMessage}>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={loading}
          className="chat-input"
        />
        <button type="submit" className="chat-send-btn" disabled={loading || !input.trim()}>
          {loading ? '...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default ChatWidget;
