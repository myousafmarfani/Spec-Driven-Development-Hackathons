// frontend/app/tasks/page.tsx
'use client';

import React, { useState, useEffect, useMemo } from 'react';
import { useSession } from '../../lib/auth';
import { getTasks, createTask, updateTask, deleteTask, toggleTaskComplete } from '../../lib/api';
import { Task, TaskCreateData, TaskUpdateData } from '../../lib/types';
import TaskList from '../../components/tasks/TaskList';
import TaskForm from '../../components/tasks/TaskForm';
import DeleteDialog from '../../components/tasks/DeleteDialog';
import Header from '../../components/layout/Header';
import { useRouter } from 'next/navigation';

type FilterType = 'all' | 'pending' | 'completed';

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [taskToDelete, setTaskToDelete] = useState<number | null>(null);
  const [filter, setFilter] = useState<FilterType>('all');
  const { data: session, isLoading: sessionLoading } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (!session && !sessionLoading) {
      router.push('/auth/signin');
    }
  }, [session, sessionLoading, router]);

  useEffect(() => {
    if (session?.user) {
      fetchTasks();
    }
  }, [session]);

  const fetchTasks = async () => {
    if (!session?.user?.id) return;
    try {
      setLoading(true);
      setError(null);
      const tasksData = await getTasks(session.user.id);
      setTasks(tasksData);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch tasks.');
    } finally {
      setLoading(false);
    }
  };

  const filteredTasks = useMemo(() => {
    if (filter === 'completed') return tasks.filter(t => t.completed);
    if (filter === 'pending') return tasks.filter(t => !t.completed);
    return tasks;
  }, [tasks, filter]);

  const stats = useMemo(() => ({
    total: tasks.length,
    completed: tasks.filter(t => t.completed).length,
    pending: tasks.filter(t => !t.completed).length,
  }), [tasks]);

  const handleCreateTask = async (taskData: TaskCreateData) => {
    if (!session?.user?.id) return;
    try {
      setSubmitting(true);
      setError(null);
      const newTask = await createTask(session.user.id, taskData);
      setTasks([newTask, ...tasks]);
      setShowForm(false);
    } catch (err: any) {
      setError(err.message || 'Failed to create task.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleUpdateTask = async (taskData: TaskUpdateData) => {
    if (!editingTask || !session?.user?.id) return;
    try {
      setSubmitting(true);
      setError(null);
      const updatedTask = await updateTask(session.user.id, editingTask.id, taskData);
      setTasks(tasks.map(task => task.id === editingTask.id ? updatedTask : task));
      setEditingTask(null);
      setShowForm(false);
    } catch (err: any) {
      setError(err.message || 'Failed to update task.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleToggleComplete = async (task: Task) => {
    if (!session?.user?.id) return;
    try {
      const updatedTask = await toggleTaskComplete(session.user.id, task.id, !task.completed);
      setTasks(tasks.map(t => t.id === task.id ? updatedTask : t));
    } catch (err: any) {
      setError(err.message || 'Failed to update task status.');
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setShowForm(true);
  };

  const handleDeleteClick = (taskId: number) => {
    setTaskToDelete(taskId);
    setShowDeleteDialog(true);
  };

  const handleDeleteConfirm = async () => {
    if (!taskToDelete || !session?.user?.id) return;
    try {
      setSubmitting(true);
      setError(null);
      await deleteTask(session.user.id, taskToDelete);
      setTasks(tasks.filter(task => task.id !== taskToDelete));
      setShowDeleteDialog(false);
      setTaskToDelete(null);
    } catch (err: any) {
      setError(err.message || 'Failed to delete task.');
      setShowDeleteDialog(false);
      setTaskToDelete(null);
    } finally {
      setSubmitting(false);
    }
  };

  const handleFormSubmit = (taskData: TaskCreateData | TaskUpdateData) => {
    if (editingTask) {
      handleUpdateTask(taskData as TaskUpdateData);
    } else {
      handleCreateTask(taskData as TaskCreateData);
    }
  };

  const cancelForm = () => {
    setShowForm(false);
    setEditingTask(null);
    setError(null);
  };

  if (sessionLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="spinner h-10 w-10" />
      </div>
    );
  }

  if (!session) return null;

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header + Stats */}
        <div className="mb-8 animate-fade-in">
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-1">My Tasks</h1>
          <p className="text-gray-500 text-sm">Stay organized. Stay productive.</p>

          {/* Stats Cards */}
          <div className="grid grid-cols-3 gap-4 mt-6">
            {[
              { label: 'Total', value: stats.total, color: 'bg-brand-50 text-brand-700 border-brand-200' },
              { label: 'Pending', value: stats.pending, color: 'bg-amber-50 text-amber-700 border-amber-200' },
              { label: 'Done', value: stats.completed, color: 'bg-emerald-50 text-emerald-700 border-emerald-200' },
            ].map(s => (
              <div key={s.label} className={`rounded-xl border p-4 ${s.color}`}>
                <p className="text-2xl font-bold">{s.value}</p>
                <p className="text-xs font-medium mt-0.5 opacity-70">{s.label}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Error Banner */}
        {error && (
          <div className="mb-6 flex items-start gap-3 p-4 rounded-xl bg-red-50 border border-red-200 animate-scale-in">
            <svg className="h-5 w-5 text-red-500 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" /></svg>
            <p className="text-sm text-red-700">{error}</p>
            <button onClick={() => setError(null)} className="ml-auto text-red-400 hover:text-red-600">
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>
        )}

        {/* Main Card */}
        <div className="card animate-slide-up">
          {/* Toolbar */}
          <div className="p-4 sm:p-6 border-b border-gray-100 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            {/* Filters */}
            <div className="flex items-center gap-1 bg-gray-100 rounded-xl p-1">
              {(['all', 'pending', 'completed'] as FilterType[]).map(f => (
                <button
                  key={f}
                  onClick={() => setFilter(f)}
                  className={`px-4 py-1.5 text-xs font-semibold rounded-lg transition-all duration-200 capitalize ${
                    filter === f
                      ? 'bg-white text-gray-900 shadow-sm'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  {f}
                </button>
              ))}
            </div>

            <button
              onClick={() => { setEditingTask(null); setShowForm(true); }}
              disabled={submitting}
              className="btn-primary text-sm"
            >
              <svg className="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" /></svg>
              New Task
            </button>
          </div>

          {/* Form */}
          {showForm && (
            <div className="p-4 sm:p-6 border-b border-gray-100 bg-gray-50/50 animate-slide-down">
              <h2 className="text-base font-semibold text-gray-900 mb-4">
                {editingTask ? 'Edit Task' : 'Create New Task'}
              </h2>
              <TaskForm
                task={editingTask || undefined}
                onSubmit={handleFormSubmit}
                onCancel={cancelForm}
                submitText={editingTask ? 'Update Task' : 'Create Task'}
              />
            </div>
          )}

          {/* Task List */}
          <div className="p-4 sm:p-6">
            {loading ? (
              <div className="flex justify-center items-center py-16">
                <div className="spinner h-8 w-8" />
              </div>
            ) : filteredTasks.length === 0 ? (
              <div className="text-center py-16">
                <div className="mx-auto h-16 w-16 rounded-2xl bg-gray-100 flex items-center justify-center mb-4">
                  <svg className="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z" />
                  </svg>
                </div>
                <h3 className="text-sm font-semibold text-gray-900 mb-1">
                  {filter !== 'all' ? `No ${filter} tasks` : 'No tasks yet'}
                </h3>
                <p className="text-sm text-gray-500 mb-6">
                  {filter !== 'all' ? 'Try a different filter.' : 'Create your first task to get started.'}
                </p>
                {filter === 'all' && (
                  <button onClick={() => { setEditingTask(null); setShowForm(true); }} className="btn-primary text-sm">
                    <svg className="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" /></svg>
                    New Task
                  </button>
                )}
              </div>
            ) : (
              <TaskList
                tasks={filteredTasks}
                onToggleComplete={handleToggleComplete}
                onEdit={handleEditTask}
                onDelete={handleDeleteClick}
              />
            )}
          </div>
        </div>
      </main>

      <DeleteDialog
        isOpen={showDeleteDialog}
        onClose={() => { setShowDeleteDialog(false); setTaskToDelete(null); }}
        onConfirm={handleDeleteConfirm}
        taskTitle={tasks.find(t => t.id === taskToDelete)?.title || ''}
      />
    </div>
  );
}