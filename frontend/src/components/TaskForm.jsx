import React, { useState, useEffect } from 'react';
import { useNotification } from './Notification';

const TaskForm = ({ onTaskCreated, taskToEdit, onEditComplete }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const { addNotification } = useNotification();

  // Populate form when taskToEdit changes
  useEffect(() => {
    if (taskToEdit) {
      setTitle(taskToEdit.title);
      setDescription(taskToEdit.description || '');
    } else {
      setTitle('');
      setDescription('');
    }
  }, [taskToEdit]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!title.trim()) {
      addNotification('Title is required', 'error');
      return;
    }

    setLoading(true);

    try {
      if (taskToEdit) {
        // Update existing task
        onEditComplete({ ...taskToEdit, title: title.trim(), description: description.trim() });
      } else {
        // Create new task
        onTaskCreated({ title: title.trim(), description: description.trim() });
        setTitle('');
        setDescription('');
      }
    } catch (err) {
      addNotification(err.message || 'An error occurred', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleCancelEdit = () => {
    onEditComplete(null);
    setTitle('');
    setDescription('');
    addNotification('Edit cancelled', 'info');
  };

  return (
    <div className="task-form">
      <h2>{taskToEdit ? 'Edit Task' : 'Create New Task'}</h2>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Title *</label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter task title"
            maxLength={255}
            required
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Enter task description (optional)"
            maxLength={10000}
            rows={3}
            disabled={loading}
          />
        </div>

        <div className="form-actions">
          {taskToEdit && (
            <button
              type="button"
              onClick={handleCancelEdit}
              className="btn btn-secondary"
              disabled={loading}
            >
              Cancel
            </button>
          )}
          <button
            type="submit"
            className={`btn ${taskToEdit ? 'btn-primary' : 'btn-success'}`}
            disabled={loading}
          >
            {loading ? 'Saving...' : (taskToEdit ? 'Update Task' : 'Create Task')}
          </button>
        </div>
      </form>
    </div>
  );
};

export default TaskForm;