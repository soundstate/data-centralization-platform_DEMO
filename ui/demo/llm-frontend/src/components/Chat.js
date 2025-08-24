import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './Chat.css';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [currentModel, setCurrentModel] = useState('microsoft/DialoGPT-medium');
  const [availableModels, setAvailableModels] = useState([]);
  const messagesEndRef = useRef(null);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001';

  useEffect(() => {
    checkConnection();
    fetchAvailableModels();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const checkConnection = async () => {
    try {
      await axios.get(`${API_BASE_URL}/health`);
      setIsConnected(true);
    } catch (error) {
      setIsConnected(false);
    }
  };

  const fetchAvailableModels = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/models`);
      setAvailableModels(response.data.available_models);
    } catch (error) {
      console.error('Failed to fetch models:', error);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = { 
      id: Date.now(), 
      text: inputMessage, 
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/chat`, {
        message: inputMessage
      });

      const assistantMessage = {
        id: Date.now() + 1,
        text: response.data.response,
        sender: 'assistant',
        timestamp: response.data.timestamp,
        model: response.data.model
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      let errorMessage = 'Sorry, something went wrong. Please try again.';
      
      if (error.response?.status === 503) {
        errorMessage = 'The model is currently loading. Please wait a moment and try again.';
      } else if (error.response?.status === 429) {
        errorMessage = 'Rate limit exceeded. Please wait a moment before sending another message.';
      }

      const errorResponse = {
        id: Date.now() + 1,
        text: errorMessage,
        sender: 'assistant',
        timestamp: new Date().toISOString(),
        isError: true
      };

      setMessages(prev => [...prev, errorResponse]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  const switchModel = async (modelName) => {
    try {
      await axios.post(`${API_BASE_URL}/api/switch-model`, { modelName });
      setCurrentModel(modelName);
    } catch (error) {
      console.error('Failed to switch model:', error);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>LLM Chat Interface</h1>
        <div className="status-indicator">
          <span className={`status-dot ${isConnected ? 'connected' : 'disconnected'}`}></span>
          <span className="status-text">
            {isConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
      </div>

      <div className="model-selector">
        <label htmlFor="model-select">Model: </label>
        <select 
          id="model-select"
          value={currentModel}
          onChange={(e) => switchModel(e.target.value)}
          disabled={isLoading}
        >
          {availableModels.map(model => (
            <option key={model.name} value={model.name}>
              {model.name} - {model.description}
            </option>
          ))}
        </select>
      </div>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <h3>Welcome to the LLM Chat Interface!</h3>
            <p>Start a conversation by typing a message below.</p>
            <p>Current model: <strong>{currentModel}</strong></p>
          </div>
        ) : (
          messages.map(message => (
            <div key={message.id} className={`message ${message.sender}`}>
              <div className="message-header">
                <span className="sender-name">
                  {message.sender === 'user' ? 'You' : 'Assistant'}
                </span>
                <span className="timestamp">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </span>
              </div>
              <div className={`message-content ${message.isError ? 'error' : ''}`}>
                {message.text}
              </div>
              {message.model && (
                <div className="model-info">
                  Model: {message.model}
                </div>
              )}
            </div>
          ))
        )}
        {isLoading && (
          <div className="message assistant">
            <div className="message-header">
              <span className="sender-name">Assistant</span>
              <span className="timestamp">typing...</span>
            </div>
            <div className="message-content loading">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <form onSubmit={sendMessage}>
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message here..."
            disabled={isLoading || !isConnected}
          />
          <button 
            type="submit" 
            disabled={isLoading || !isConnected || !inputMessage.trim()}
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </form>
        <button 
          type="button" 
          onClick={clearChat}
          className="clear-button"
          disabled={messages.length === 0}
        >
          Clear Chat
        </button>
      </div>
    </div>
  );
};

export default Chat;
