import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

export const listTasks = () => api.get('/api/tasks').then((res) => res.data);

export const createTask = (task) => api.post('/api/tasks', task).then((res) => res.data);

export const updateTask = (id, updates) =>
  api.patch(`/api/tasks/${id}`, updates).then((res) => res.data);

export const deleteTask = (id) => api.delete(`/api/tasks/${id}`);
