import React, { useState } from 'react';
import { useTasks } from '../contexts/TasksContext';
import { useAuth } from '../auth/auth_provider';
import TaskList from '../components/TaskList';
import TaskForm from '../components/TaskForm';
import ChatInterface from '../components/ChatInterface';
import Link from 'next/link';

const HomePage = () => {
  const { createTask, updateTask, deleteTask } = useTasks();
  const { user, isAuthenticated, isLoading, logout } = useAuth();
  const [taskToEdit, setTaskToEdit] = useState(null);

  // Show loading state while checking authentication
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <h1 className="text-center text-3xl font-extrabold text-gray-900">
            Todo App
          </h1>
          <p className="mt-2 text-center text-sm text-gray-600">
            Please sign in to access your tasks
          </p>
        </div>

        <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
            <div className="flex flex-col space-y-4">
              <Link href="/login">
                <button className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                  Sign In
                </button>
              </Link>
              <Link href="/register">
                <button className="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                  Create Account
                </button>
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const handleTaskCreated = async (newTask) => {
    try {
      await createTask(newTask);
    } catch (error) {
      // Error handling is done in the context
    }
  };

  const handleTaskUpdated = async (updatedTask) => {
    try {
      await updateTask(updatedTask.id, updatedTask);
    } catch (error) {
      // Error handling is done in the context
    }
    setTaskToEdit(null);
  };

  const handleEditTask = (task) => {
    setTaskToEdit(task);
  };

  const handleDeleteTask = async (taskId) => {
    try {
      await deleteTask(taskId);
    } catch (error) {
      // Error handling is done in the context
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="app-header mb-8">
        <div className="flex justify-between items-center w-full mb-4">
          <div>
            <h1 className="app-title text-3xl font-bold text-gray-900">Todo Application</h1>
            <p className="app-subtitle text-gray-600">Welcome back, {user?.email}!</p>
          </div>
          <div>
            <button
              onClick={logout}
              className="flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Logout
            </button>
          </div>
        </div>
        <p className="app-subtitle text-gray-600">Manage your tasks efficiently with real-time updates</p>
      </div>

      <div className="app-content grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left Column: Task Form and Task List */}
        <div className="left-column space-y-8">
          <div className="form-section">
            <div className="bg-white p-6 rounded-lg shadow">
              <h2 className="text-xl font-semibold mb-4">Add New Task</h2>
              <TaskForm
                onTaskCreated={handleTaskCreated}
                taskToEdit={taskToEdit}
                onEditComplete={handleTaskUpdated}
              />
            </div>
          </div>

          <div className="list-section">
            <div className="bg-white p-6 rounded-lg shadow">
              <h2 className="text-xl font-semibold mb-4">Your Tasks</h2>
              <TaskList
                onTaskUpdate={handleEditTask}
                onTaskDelete={handleDeleteTask}
              />
            </div>
          </div>
        </div>

        {/* Right Column: AI Chat Interface */}
        <div className="right-column">
          <div className="bg-white p-6 rounded-lg shadow h-full">
            <h2 className="text-xl font-semibold mb-4">AI Todo Assistant</h2>
            <ChatInterface />
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;