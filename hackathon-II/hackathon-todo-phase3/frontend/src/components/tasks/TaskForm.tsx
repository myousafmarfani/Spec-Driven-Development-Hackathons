// frontend/components/tasks/TaskForm.tsx
'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Task, TaskCreateData, TaskUpdateData } from '../../lib/types';

interface TaskFormProps {
  task?: Task;
  onSubmit: (taskData: TaskCreateData | TaskUpdateData) => void;
  onCancel: () => void;
  submitText?: string;
}

const TaskForm: React.FC<TaskFormProps> = ({ task, onSubmit, onCancel, submitText = 'Save Task' }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>('medium');
  const [dueDate, setDueDate] = useState('');
  const [error, setError] = useState('');
  const titleRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (task) {
      setTitle(task.title);
      setDescription(task.description || '');
      setPriority(task.priority || 'medium');
      setDueDate(task.due_date ? task.due_date.slice(0, 10) : '');
    } else {
      setTitle('');
      setDescription('');
      setPriority('medium');
      setDueDate('');
      setError('');
    }
    titleRef.current?.focus();
  }, [task]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) { setError('Title is required'); return; }
    if (title.length > 200) { setError('Title must be 200 characters or less'); return; }
    if (description && description.length > 1000) { setError('Description must be 1000 characters or less'); return; }
    setError('');
    onSubmit({
      title: title.trim(),
      description: description.trim(),
      priority,
      due_date: dueDate ? new Date(dueDate).toISOString() : undefined,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="title" className="block text-xs font-semibold text-gray-700 mb-1.5">
          Title <span className="text-red-400">*</span>
        </label>
        <input
          ref={titleRef}
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="input-field"
          placeholder="What needs to be done?"
          maxLength={200}
        />
        <div className="flex justify-between mt-1">
          <p className="text-[11px] text-gray-400">Required</p>
          <p className={`text-[11px] ${title.length > 180 ? 'text-amber-500' : 'text-gray-400'}`}>{title.length}/200</p>
        </div>
      </div>

      <div>
        <label htmlFor="description" className="block text-xs font-semibold text-gray-700 mb-1.5">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="input-field resize-none"
          placeholder="Add more details (optional)"
          rows={3}
          maxLength={1000}
        />
        <div className="flex justify-end mt-1">
          <p className={`text-[11px] ${description.length > 900 ? 'text-amber-500' : 'text-gray-400'}`}>{description.length}/1000</p>
        </div>
      </div>

      {/* Priority & Due Date Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label className="block text-xs font-semibold text-gray-700 mb-1.5">
            Priority
          </label>
          <div className="flex items-center gap-1 bg-gray-100 rounded-xl p-1">
            {(['low', 'medium', 'high'] as const).map(p => (
              <button
                key={p}
                type="button"
                onClick={() => setPriority(p)}
                className={`flex-1 px-3 py-1.5 text-xs font-semibold rounded-lg transition-all duration-200 capitalize ${
                  priority === p
                    ? p === 'high'
                      ? 'bg-white text-red-600 shadow-sm'
                      : p === 'medium'
                        ? 'bg-white text-amber-600 shadow-sm'
                        : 'bg-white text-emerald-600 shadow-sm'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                {p}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label htmlFor="dueDate" className="block text-xs font-semibold text-gray-700 mb-1.5">
            Due Date
          </label>
          <input
            type="date"
            id="dueDate"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            className="input-field"
          />
        </div>
      </div>

      {error && (
        <div className="flex items-center gap-2 p-3 rounded-lg bg-red-50 border border-red-200">
          <svg className="h-4 w-4 text-red-500 shrink-0" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" /></svg>
          <p className="text-xs text-red-600 font-medium">{error}</p>
        </div>
      )}

      <div className="flex items-center gap-3 pt-2">
        <button type="submit" className="btn-primary text-sm">
          {submitText}
        </button>
        <button type="button" onClick={onCancel} className="btn-secondary text-sm">
          Cancel
        </button>
      </div>
    </form>
  );
};

export default TaskForm;