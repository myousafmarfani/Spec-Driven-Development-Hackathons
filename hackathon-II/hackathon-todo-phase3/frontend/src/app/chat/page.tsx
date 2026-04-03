// frontend/src/app/chat/page.tsx
'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useSession } from '../../lib/auth';
import Header from '../../components/layout/Header';
import { useRouter } from 'next/navigation';
import { getConversationMessages } from '../../lib/api';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { data: session, isLoading: sessionLoading } = useSession();
  const router = useRouter();

  // Redirect to sign-in if not authenticated
  useEffect(() => {
    if (!session && !sessionLoading) {
      router.push('/auth/signin');
    }
  }, [session, sessionLoading, router]);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Load conversation history from API
  const loadConversationHistory = useCallback(async (convId: string, userId: string) => {
    setIsLoadingHistory(true);
    setError(null);
    try {
      const data = await getConversationMessages(userId, convId);
      const loadedMessages: Message[] = data.messages.map((msg) => ({
        id: `${msg.id}`,
        role: msg.role as 'user' | 'assistant',
        content: msg.content,
        timestamp: new Date(msg.created_at),
      }));
      setMessages(loadedMessages);
    } catch (err) {
      console.error('Error loading conversation history:', err);
      // If conversation not found, clear the stored ID and start fresh
      if (err instanceof Error && err.message === 'Conversation not found') {
        localStorage.removeItem('conversation_id');
        setConversationId(null);
      } else {
        setError('Failed to load conversation history. Starting a new conversation.');
        localStorage.removeItem('conversation_id');
        setConversationId(null);
      }
    } finally {
      setIsLoadingHistory(false);
    }
  }, []);

  // Load stored conversation ID on mount and fetch messages
  useEffect(() => {
    const storedId = localStorage.getItem('conversation_id');
    if (storedId && session?.user?.id) {
      setConversationId(storedId);
      loadConversationHistory(storedId, session.user.id);
    }
  }, [session?.user?.id, loadConversationHistory]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || !session?.user?.id) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputValue;
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem('jwt_token') || '';
      const response = await fetch(`${API_URL}/api/${session.user.id}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: currentInput,
          conversation_id: conversationId,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      setConversationId(data.conversation_id);
      localStorage.setItem('conversation_id', data.conversation_id);

      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      setError('Failed to send message. Please try again.');

      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  if (sessionLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="spinner h-8 w-8" />
      </div>
    );
  }

  if (!session) return null;

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Header />

      <main className="flex-1 flex flex-col max-w-4xl w-full mx-auto px-4 py-6">
        {/* Chat Header */}
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Todo Assistant</h1>
            <p className="text-sm text-gray-500">Chat with AI to manage your tasks</p>
          </div>
        </div>

        {/* Chat Card */}
        <div className="card flex flex-col flex-1 min-h-0">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4" style={{ maxHeight: 'calc(100vh - 320px)' }}>
            {/* Loading history state */}
            {isLoadingHistory && (
              <div className="flex flex-col items-center justify-center h-full text-center py-16">
                <div className="h-16 w-16 rounded-2xl bg-brand-50 flex items-center justify-center mb-4">
                  <div className="spinner h-8 w-8" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">Loading conversation...</h3>
                <p className="text-sm text-gray-500">Retrieving your message history</p>
              </div>
            )}

            {/* Empty state */}
            {messages.length === 0 && !isLoading && !isLoadingHistory && (
              <div className="flex flex-col items-center justify-center h-full text-center py-16">
                <div className="h-16 w-16 rounded-2xl bg-brand-50 flex items-center justify-center mb-4">
                  <svg className="h-8 w-8 text-brand-500" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M8.625 9.75a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375m-13.5 3.01c0 1.6 1.123 2.994 2.707 3.227 1.087.16 2.185.283 3.293.369V21l4.184-4.183a1.14 1.14 0 01.778-.332 48.294 48.294 0 005.83-.498c1.585-.233 2.708-1.626 2.708-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">Start a conversation</h3>
                <p className="text-sm text-gray-500 max-w-sm">
                  Ask me to add, list, complete, update, or delete your tasks. For example: &quot;Add a task to buy groceries&quot;
                </p>
              </div>
            )}

            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[75%] px-4 py-2.5 rounded-2xl ${
                    message.role === 'user'
                      ? 'bg-brand-600 text-white rounded-br-md'
                      : 'bg-gray-100 text-gray-800 rounded-bl-md'
                  }`}
                >
                  <div className="whitespace-pre-wrap text-sm">{message.content}</div>
                  <div
                    className={`text-[10px] mt-1 ${
                      message.role === 'user' ? 'text-brand-200' : 'text-gray-400'
                    }`}
                  >
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 text-gray-800 px-4 py-3 rounded-2xl rounded-bl-md">
                  <div className="flex space-x-1.5">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="border-t border-gray-100 p-4">
            {error && (
              <div className="flex items-center gap-2 text-red-600 text-sm mb-3 p-2 bg-red-50 rounded-lg">
                <svg className="h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
                </svg>
                {error}
              </div>
            )}
            <form onSubmit={handleSubmit} className="flex gap-2">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Type your message..."
                className="input-field flex-1"
                disabled={isLoading || isLoadingHistory}
              />
              <button
                type="submit"
                disabled={isLoading || isLoadingHistory || !inputValue.trim()}
                className="btn-primary !px-4 !py-3"
              >
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
                </svg>
              </button>
            </form>
          </div>
        </div>
      </main>
    </div>
  );
}
