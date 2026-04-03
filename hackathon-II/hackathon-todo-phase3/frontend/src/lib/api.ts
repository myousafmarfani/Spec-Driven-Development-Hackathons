// frontend/lib/api.ts
import { getToken } from './auth';

/**
 * API client wrapper for communicating with the backend API
 */

interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  due_date?: string;
  created_at: string;
  updated_at: string;
}

interface TaskCreateData {
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high';
  due_date?: string;
}

interface TaskUpdateData {
  title?: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high';
  due_date?: string;
}

// Get JWT token from auth utility
const getAuthHeaders = () => {
  const token = getToken();
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };
};

/**
 * Get all tasks for a user
 */
export const getTasks = async (userId: string, status?: string): Promise<Task[]> => {
  try {
    const headers = getAuthHeaders();
    let url = `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/${userId}/tasks`;

    if (status) {
      url += `?status=${encodeURIComponent(status)}`;
    }

    const response = await fetch(url, {
      method: 'GET',
      headers,
    });

    if (!response.ok) {
      throw new Error(`Failed to get tasks: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error getting tasks:', error);
    throw error;
  }
};

/**
 * Create a new task for a user
 */
export const createTask = async (userId: string, data: TaskCreateData): Promise<Task> => {
  try {
    const headers = getAuthHeaders();
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/${userId}/tasks`, {
      method: 'POST',
      headers,
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`Failed to create task: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error creating task:', error);
    throw error;
  }
};

/**
 * Get a specific task
 */
export const getTask = async (userId: string, taskId: number): Promise<Task> => {
  try {
    const headers = getAuthHeaders();
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/${userId}/tasks/${taskId}`, {
      method: 'GET',
      headers,
    });

    if (!response.ok) {
      throw new Error(`Failed to get task: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error getting task:', error);
    throw error;
  }
};

/**
 * Update a task
 */
export const updateTask = async (userId: string, taskId: number, data: TaskUpdateData): Promise<Task> => {
  try {
    const headers = getAuthHeaders();
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      headers,
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`Failed to update task: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error updating task:', error);
    throw error;
  }
};

/**
 * Delete a task
 */
export const deleteTask = async (userId: string, taskId: number): Promise<void> => {
  try {
    const headers = getAuthHeaders();
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
      headers,
    });

    if (!response.ok) {
      throw new Error(`Failed to delete task: ${response.statusText}`);
    }
  } catch (error) {
    console.error('Error deleting task:', error);
    throw error;
  }
};

/**
 * Toggle task completion status
 */
export const toggleTaskComplete = async (userId: string, taskId: number, completed: boolean): Promise<Task> => {
  try {
    const headers = getAuthHeaders();
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
      headers,
      body: JSON.stringify({ completed }),
    });

    if (!response.ok) {
      throw new Error(`Failed to toggle task completion: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error toggling task completion:', error);
    throw error;
  }
};

// ============================================
// Chat/Conversation API
// ============================================

interface ChatMessage {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

interface ConversationMessagesResponse {
  conversation_id: string;
  messages: ChatMessage[];
}

/**
 * Get all messages for a conversation
 */
export const getConversationMessages = async (
  userId: string,
  conversationId: string
): Promise<ConversationMessagesResponse> => {
  try {
    const headers = getAuthHeaders();
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/${userId}/conversations/${conversationId}/messages`,
      {
        method: 'GET',
        headers,
      }
    );

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Conversation not found');
      }
      throw new Error(`Failed to get conversation messages: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error getting conversation messages:', error);
    throw error;
  }
};