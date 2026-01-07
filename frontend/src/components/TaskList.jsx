import React from 'react';
import { useNotification } from './Notification';
import { useTasks } from '../contexts/TasksContext';

const TaskList = ({ onTaskUpdate, onTaskDelete }) => {
  const { tasks, loading, error, toggleTaskCompletion, deleteTask } = useTasks();
  const { addNotification } = useNotification();

  const handleToggleCompletion = async (task) => {
    try {
      await toggleTaskCompletion(task);
      if (onTaskUpdate) onTaskUpdate(task);
    } catch (err) {
      // Error handling is done in the context
    }
  };

  const handleDeleteTask = async (task) => {
    try {
      await deleteTask(task.id);
      if (onTaskDelete) onTaskDelete(task.id);
    } catch (err) {
      // Error handling is done in the context
    }
  };

  if (loading) return <div className="loading">Loading tasks...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="task-list">
      <h2>Tasks</h2>
      {tasks.length === 0 ? (
        <div className="empty-state">
          <h3>No tasks yet</h3>
          <p>Create your first task to get started!</p>
        </div>
      ) : (
        <ul className="task-list-ul">
          {tasks.map(task => (
            <li key={task.id} className={`task-item ${task.is_completed ? 'completed' : ''}`}>
              <div className="task-content">
                <input
                  type="checkbox"
                  checked={task.is_completed}
                  onChange={() => handleToggleCompletion(task)}
                  className="task-checkbox"
                  aria-label={task.is_completed ? `Mark ${task.title} as incomplete` : `Mark ${task.title} as complete`}
                />
                <div className="task-text">
                  <h3>{task.title}</h3>
                  {task.description && <p>{task.description}</p>}
                  <div className="task-meta">
                    <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
                    <span>Updated: {new Date(task.updated_at).toLocaleDateString()}</span>
                  </div>
                </div>
              </div>
              <div className="task-actions">
                <button
                  onClick={() => onTaskUpdate && onTaskUpdate(task)}
                  className="btn btn-secondary"
                  aria-label={`Edit task: ${task.title}`}
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDeleteTask(task)}
                  className="btn btn-error"
                  aria-label={`Delete task: ${task.title}`}
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TaskList;