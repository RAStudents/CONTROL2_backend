import { config } from './config.js';

const TOKEN_KEY = 'control_token';

export const api = {
  // Сохраняем токен после логина
  setToken(token) {
    localStorage.setItem(TOKEN_KEY, token);
  },

  // Получаем токен для запросов
  getToken() {
    return localStorage.getItem(TOKEN_KEY);
  },

  // Выход
  logout() {
    localStorage.removeItem(TOKEN_KEY);
  },

  // Базовый метод для запросов
  async request(endpoint, options = {}) {
    const url = `${config.apiUrl}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...(this.getToken() ? { 'Authorization': `Bearer ${this.getToken()}` } : {}),
      ...options.headers,
    };

    const response = await fetch(url, { ...options, headers });

    if (response.status === 401) {
      this.logout();
      window.location.reload(); // Если токен протух, выкидываем на логин
      throw new Error('Неавторизован');
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Ошибка сервера');
    }

    return response.json();
  },

  // Авторизация
  async login(email, password) {
    const data = await this.request('/api/cabinet/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    this.setToken(data.access_token);
    return data;
  },

  // Получение событий (пока эндпоинта нет, вернем пустой массив, но потом добавим)
  async getEvents() {
    // Когда сделаем эндпоинт /api/cabinet/feed, раскомментируем:
    return this.request('/api/cabinet/feed');
    return []; 
  }
};