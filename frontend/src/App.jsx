import { useState } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from 'recharts';

const App = () => {
  const [file, setFile] = useState(null);
  const [user, setUser] = useState('');
  const [name, setName] = useState('');
  const [intervalsDashboard, setIntervalsDashboard] = useState(null);
  const [whoTextedMoreDashboard, setWhoTextedMoreDashboard] = useState(null);
  const [interval, setInterval] = useState(0);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmitData = async () => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user', user);
    formData.append('name', 'ксюша');

    if (!file) {
      alert('Пожалуйста, выберите файл перед отправкой');
      return;
    }

    try {
      await axios.post(
        'http://127.0.0.1:8000/v1/files/upload_file/?user=' + encodeURIComponent(user) + '&name=' + encodeURIComponent('ксюша'), 
        formData, 
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      alert('Данные успешно отправлены!');
    } catch (error) {
      console.error('Ошибка при отправке данных:', error);
      alert('Ошибка при отправке данных');
    }
  };

  const handleGetIntervalsDashboard = async () => {
    try {
      const numericalInterval = parseInt(interval, 10);

      const response = await axios.post('http://127.0.0.1:8000/v1/data/get_intervals/', 
        { user, name, interval: numericalInterval });
        setIntervalsDashboard(response.data);
    } catch (error) {
      console.error('Error while getting mean intervals dashboard data:', error);
    }
  };

  const handleGetWhoTextedMoreDashboard = async () => {
    try {
      const numericalInterval = parseInt(interval, 10);

      const response = await axios.post('http://127.0.0.1:8000/v1/data/who_texted_more/', 
        { user, name, interval: numericalInterval });
        setWhoTextedMoreDashboard(response.data);
    } catch (error) {
      console.error('Ошибка при получении второго дашборда:', error);
    }
  };

  return (
    <div className="App">
      <h1>Статистика вашего чата в Telegram</h1>
      <input type="file" onChange={handleFileChange} />
      <input 
        type="text" 
        placeholder="Имя пользователя" 
        value={user} 
        onChange={(e) => setUser(e.target.value)} 
      />
      <input 
        type="text" 
        placeholder="Имя" 
        value={name} 
        onChange={(e) => setName(e.target.value)} 
      />
      <input 
        type="number" 
        placeholder="Интервал (число)" 
        value={interval} 
        onChange={(e) => setInterval(e.target.value)} 
      />
      <button onClick={handleSubmitData}>Отправить данные</button>
      <button onClick={handleGetIntervalsDashboard}>Получить график средних интервалов в общении</button>
      <button onClick={handleGetWhoTextedMoreDashboard}>Получить график количества сообщений</button>

      {intervalsDashboard && (
        <div>
          <h2>Средние за каждые {interval} дней интервалы в общении</h2>
          <LineChart width={600} height={300} data={Object.entries(intervalsDashboard.metric_1 || {}).map(([date, value]) => ({ date, value, metric_2: intervalsDashboard.metric_2[date] }))}>
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <CartesianGrid strokeDasharray="3 3" />
            <Legend />
            <Line type="monotone" dataKey="value" stroke="blue" name="Вы" />
            <Line type="monotone" dataKey="metric_2" stroke="red" name="Собеседник" />
          </LineChart>
        </div>
      )}
      
      {whoTextedMoreDashboard && (
        <div>
          <h2>Количество сообщений за каждые {interval} дней</h2>
          <LineChart width={600} height={300} data={Object.entries(whoTextedMoreDashboard.metric_1 || {}).map(([date, value]) => ({ date, value, metric_2: whoTextedMoreDashboard.metric_2[date] }))}>
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <CartesianGrid strokeDasharray="3 3" />
            <Legend />
            <Line type="monotone" dataKey="value" stroke="blue" name="Вы" />
            <Line type="monotone" dataKey="metric_2" stroke="red" name="Собеседник" />
          </LineChart>
        </div>
      )}
    </div>
  );
};

export default App;
