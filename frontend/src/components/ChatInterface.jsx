import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../auth/auth_provider';
import axios from 'axios';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const { user } = useAuth();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputValue.trim() || !user) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Send message to backend API with authorization header
      const baseURL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';
      const token = localStorage.getItem('auth_token');
      const response = await axios.post(`${baseURL}/api/${user.id}/chat`, {
        message: inputValue
      }, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      const botMessage = {
        id: Date.now() + 1,
        text: response.data.response,
        sender: 'bot',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error processing your request.',
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-container bg-white p-6 rounded-lg shadow h-full flex flex-col">
      <div className="chat-header mb-4">
        <h3 className="text-lg font-semibold text-gray-800">AI Todo Assistant</h3>
        <p className="text-sm text-gray-600">Ask me to manage your tasks with natural language</p>
      </div>

      <div className="messages-container flex-grow overflow-y-auto max-h-96 mb-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-64 text-gray-500">
            <p className="mb-2">Hello! I'm your AI Todo Assistant.</p>
            <p className="text-sm">Try saying things like:</p>
            <ul className="text-xs mt-2 text-left">
              <li>"Add a task to buy groceries"</li>
              <li>"Show me my tasks"</li>
              <li>"Mark task 1 as completed"</li>
              <li>"Delete my meeting task"</li>
            </ul>
          </div>
        ) : (
          <div className="space-y-3">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                    message.sender === 'user'
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-200 text-gray-800'
                  }`}
                >
                  <div className="text-sm">{message.text}</div>
                  <div className={`text-xs mt-1 ${message.sender === 'user' ? 'text-blue-200' : 'text-gray-500'}`}>
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-200 text-gray-800 px-4 py-2 rounded-lg max-w-xs">
                  <div className="text-sm">Thinking...</div>
                </div>
              </div>
            )}
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-container">
        <div className="flex space-x-2">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message here..."
            className="flex-grow border border-gray-300 rounded-lg p-2 resize-none"
            rows="2"
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={isLoading || !inputValue.trim()}
            className={`px-4 py-2 rounded-lg ${
              isLoading || !inputValue.trim()
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-500 text-white hover:bg-blue-600'
            }`}
          >
            Send
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Examples: "Add task: Buy milk", "Show my tasks", "Complete task 1"
        </p>
      </div>
    </div>
  );
};

export default ChatInterface;