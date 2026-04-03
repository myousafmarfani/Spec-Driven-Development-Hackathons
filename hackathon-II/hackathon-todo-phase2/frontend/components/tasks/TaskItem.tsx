// frontend/components/tasks/TaskItem.tsx
'use client';

import React from 'react';
import { Task } from '../../lib/types';

interface TaskItemProps {
  task: Task;
  onToggleComplete: () => void;
  onEdit: () => void;
  onDelete: () => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onToggleComplete, onEdit, onDelete }) => {
  const timeAgo = (dateStr: string) => {
    const diff = Date.now() - new Date(dateStr).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 1) return 'just now';
    if (mins < 60) return `${mins}m ago`;
    const hours = Math.floor(mins / 60);
    if (hours < 24) return `${hours}h ago`;
    const days = Math.floor(hours / 24);
    return `${days}d ago`;
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  const priorityConfig = {
    high:   { label: 'High',   bg: 'bg-red-50',     text: 'text-red-600',     dot: 'bg-red-400' },
    medium: { label: 'Medium', bg: 'bg-amber-50',   text: 'text-amber-600',   dot: 'bg-amber-400' },
    low:    { label: 'Low',    bg: 'bg-emerald-50', text: 'text-emerald-600', dot: 'bg-emerald-400' },
  };

  const priority = priorityConfig[task.priority] || priorityConfig.medium;

  const isDueSoon = task.due_date && !task.completed && (() => {
    const diff = new Date(task.due_date!).getTime() - Date.now();
    return diff < 86400000 * 2; // within 2 days
  })();

  const isOverdue = task.due_date && !task.completed && new Date(task.due_date).getTime() < Date.now();

  return (
    <li className="group py-3 transition-all duration-200">
      <div className="flex items-start gap-3">
        {/* Custom Checkbox */}
        <button
          onClick={onToggleComplete}
          className={`mt-0.5 flex-shrink-0 h-5 w-5 rounded-md border-2 flex items-center justify-center transition-all duration-200 ${
            task.completed
              ? 'bg-emerald-500 border-emerald-500'
              : 'border-gray-300 hover:border-brand-400 group-hover:border-brand-300'
          }`}
        >
          {task.completed && (
            <svg className="h-3 w-3 text-white" fill="none" viewBox="0 0 24 24" strokeWidth="3" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
            </svg>
          )}
        </button>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <p className={`text-sm font-medium transition-all duration-200 ${
              task.completed ? 'line-through text-gray-400' : 'text-gray-900'
            }`}>
              {task.title}
            </p>
            <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold ${
              task.completed
                ? 'bg-emerald-50 text-emerald-600'
                : 'bg-amber-50 text-amber-600'
            }`}>
              {task.completed ? 'Done' : 'Pending'}
            </span>
            <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold ${priority.bg} ${priority.text}`}>
              <span className={`h-1.5 w-1.5 rounded-full ${priority.dot}`} />
              {priority.label}
            </span>
          </div>
          {task.description && (
            <p className={`mt-0.5 text-xs leading-relaxed ${
              task.completed ? 'text-gray-300 line-through' : 'text-gray-500'
            }`}>
              {task.description}
            </p>
          )}
          <div className="mt-1 flex items-center gap-3 flex-wrap">
            <p className="text-[11px] text-gray-400">
              Created {formatDate(task.created_at)}
              {task.updated_at !== task.created_at && ` · edited`}
            </p>
            {task.due_date && (
              <p className={`text-[11px] font-medium flex items-center gap-1 ${
                isOverdue
                  ? 'text-red-500'
                  : isDueSoon
                    ? 'text-amber-500'
                    : task.completed
                      ? 'text-gray-400'
                      : 'text-gray-500'
              }`}>
                <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" />
                </svg>
                {isOverdue ? 'Overdue · ' : isDueSoon ? 'Due soon · ' : 'Due '}{formatDate(task.due_date)}
              </p>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
          <button
            onClick={onEdit}
            className="p-1.5 rounded-lg text-gray-400 hover:text-brand-600 hover:bg-brand-50 transition-colors"
            title="Edit task"
          >
            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
            </svg>
          </button>
          <button
            onClick={onDelete}
            className="p-1.5 rounded-lg text-gray-400 hover:text-red-600 hover:bg-red-50 transition-colors"
            title="Delete task"
          >
            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
            </svg>
          </button>
        </div>
      </div>
    </li>
  );
};

export default TaskItem;