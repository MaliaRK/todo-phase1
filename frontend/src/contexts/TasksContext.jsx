import React, { createContext, useContext, useReducer, useEffect } from 'react';
import ApiClient from '../services/api_client';
import { useNotification } from '../components/Notification';

const TasksContext = createContext();

const tasksReducer = (state, action) => {
  switch (action.type) {
    case 'SET_TASKS':
      return {
        ...state,
        tasks: action.payload,
        loading: false
      };
    case 'SET_LOADING':
      return {
        ...state,
        loading: action.payload
      };
    case 'ADD_TASK':
      return {
        ...state,
        tasks: [...state.tasks, action.payload]
      };
    case 'UPDATE_TASK':
      return {
        ...state,
        tasks: state.tasks.map(task =>
          task.id === action.payload.id ? action.payload : task
        )
      };
    case 'DELETE_TASK':
      return {
        ...state,
        tasks: state.tasks.filter(task => task.id !== action.payload)
      };
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
        loading: false
      };
    default:
      return state;
  }
};

export const TasksProvider = ({ children }) => {
  const [state, dispatch] = useReducer(tasksReducer, {
    tasks: [],
    loading: true,
    error: null
  });

  const { addNotification } = useNotification();

  useEffect(() => {
    fetchTasks();
  }, []); // Empty dependency array is correct

  const fetchTasks = async () => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const data = await ApiClient.getTasks();
      dispatch({ type: 'SET_TASKS', payload: data });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: 'Failed to load tasks' });
      addNotification('Failed to load tasks', 'error');
    }
  };

  const createTask = async (taskData) => {
    try {
      const newTask = await ApiClient.createTask(taskData);
      dispatch({ type: 'ADD_TASK', payload: newTask });
      addNotification(`Task "${newTask.title}" created successfully!`, 'success');
      return newTask;
    } catch (error) {
      addNotification('Failed to create task', 'error');
      throw error;
    }
  };

  const updateTask = async (id, taskData) => {
    try {
      const updatedTask = await ApiClient.updateTask(id, taskData);
      dispatch({ type: 'UPDATE_TASK', payload: updatedTask });
      addNotification(`Task "${updatedTask.title}" updated successfully!`, 'success');
      return updatedTask;
    } catch (error) {
      addNotification('Failed to update task', 'error');
      throw error;
    }
  };

  const deleteTask = async (id) => {
    try {
      const task = state.tasks.find(t => t.id === id);
      await ApiClient.deleteTask(id);
      dispatch({ type: 'DELETE_TASK', payload: id });
      if (task) {
        addNotification(`Task "${task.title}" deleted successfully!`, 'success');
      }
    } catch (error) {
      addNotification('Failed to delete task', 'error');
      throw error;
    }
  };

  const toggleTaskCompletion = async (task) => {
    try {
      const updatedTask = await ApiClient.toggleTaskCompletion(task.id);
      dispatch({ type: 'UPDATE_TASK', payload: updatedTask });

      const message = updatedTask.is_completed
        ? `Task "${updatedTask.title}" marked as completed!`
        : `Task "${updatedTask.title}" marked as incomplete!`;

      addNotification(message, 'success');
      return updatedTask;
    } catch (error) {
      addNotification('Failed to update task completion status', 'error');
      throw error;
    }
  };

  const value = {
    ...state,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion
  };

  return (
    <TasksContext.Provider value={value}>
      {children}
    </TasksContext.Provider>
  );
};

export const useTasks = () => {
  const context = useContext(TasksContext);
  if (!context) {
    throw new Error('useTasks must be used within a TasksProvider');
  }
  return context;
};