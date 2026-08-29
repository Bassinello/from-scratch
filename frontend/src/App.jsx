import { useEffect, useState } from 'react';
import { listTasks, createTask, updateTask, deleteTask } from './api';
import './App.css';

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');

  const loadTasks = async () => {
    try {
      const data = await listTasks();
      setTasks(data);
    } catch {
      setError('Não foi possível carregar as tarefas. O backend está rodando?');
    }
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim() || !description.trim()) return;
    await createTask({ title, description });
    setTitle('');
    setDescription('');
    loadTasks();
  };

  const handleToggle = async (task) => {
    await updateTask(task._id, { completed: !task.completed });
    loadTasks();
  };

  const handleDelete = async (id) => {
    await deleteTask(id);
    loadTasks();
  };

  return (
    <>
      <section id="tasks">
        <h1>Minhas Tarefas</h1>

        {error && <p className="error">{error}</p>}

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Título"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
          <input
            type="text"
            placeholder="Descrição"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
          <button type="submit">Adicionar</button>
        </form>

        <ul>
          {tasks.map((task) => (
            <li key={task._id} className={task.completed ? 'done' : ''}>
              <label>
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => handleToggle(task)}
                />
                <strong>{task.title}</strong> — {task.description}
              </label>
              <button type="button" onClick={() => handleDelete(task._id)}>
                Excluir
              </button>
            </li>
          ))}
        </ul>

        {tasks.length === 0 && !error && (
          <p>Nenhuma tarefa ainda. Crie a primeira acima.</p>
        )}
      </section>
    </>
  );
}

export default App;
