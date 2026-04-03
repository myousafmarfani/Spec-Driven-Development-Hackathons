import React, { useState, useEffect } from 'react';
import ChatKit from '../chat/ChatKit';
import { useRouter } from 'next/router';

const ChatPage: React.FC = () => {
  const router = useRouter();
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    // Get user ID from wherever it's stored (could be from auth context, local storage, etc.)
    // For now, we'll simulate getting it from localStorage or a mock user
    const storedUserId = localStorage.getItem('user_id');
    if (storedUserId) {
      setUserId(storedUserId);
    } else {
      // Redirect to login if no user is found
      router.push('/login');
    }
  }, [router]);

  if (!userId) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <p className="text-lg text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="p-6">
            <h1 className="text-2xl font-bold text-gray-800 mb-2">Todo Assistant Chat</h1>
            <p className="text-gray-600 mb-6">Chat with our AI assistant to manage your tasks</p>

            <div className="h-[600px]">
              <ChatKit userId={userId} />
            </div>
          </div>
        </div>

        <div className="mt-6 text-center text-sm text-gray-500">
          <p>Powered by OpenAI and your Todo Management System</p>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;