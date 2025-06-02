import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';

// Use import.meta.env for Vite compatibility
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor to include auth token
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor to handle token refresh
    this.api.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as any;
        
        // If error is 401 and we haven't already tried to refresh the token
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;
          
          try {
            const refreshToken = localStorage.getItem('refresh_token');
            if (!refreshToken) {
              // No refresh token, redirect to login
              window.location.href = '/login';
              return Promise.reject(error);
            }
            
            // Try to refresh the token
            const response = await axios.post(`${API_URL}/auth/token/refresh/`, {
              refresh: refreshToken,
            });
            
            const { access, refresh } = response.data;
            
            // Update tokens in storage
            localStorage.setItem('access_token', access);
            if (refresh) {
              localStorage.setItem('refresh_token', refresh);
            }
            
            // Update the Authorization header
            originalRequest.headers.Authorization = `Bearer ${access}`;
            
            // Retry the original request
            return this.api(originalRequest);
          } catch (refreshError) {
            // If refresh fails, clear tokens and redirect to login
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/login';
            return Promise.reject(refreshError);
          }
        }
        
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async login(credentials: { email: string; password: string }) {
    const response = await this.api.post('/auth/token/', {
      email: credentials.email,
      password: credentials.password,
    });
    
    const { access, refresh, user } = response.data;
    
    // Store tokens
    localStorage.setItem('access_token', access);
    if (refresh) {
      localStorage.setItem('refresh_token', refresh);
    }
    
    return { user, token: access };
  }

  async getCurrentUser() {
    const response = await this.api.get('/auth/me/');
    return response.data;
  }
  
  async logout() {
    // Clear tokens
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  // Family endpoints
  async getFamilies(params?: Record<string, any>) {
    const response = await this.api.get('/familias/', { params });
    return response.data;
  }

  async getFamily(id: number) {
    const response = await this.api.get(`/familias/${id}/`);
    return response.data;
  }

  async createFamily(data: any) {
    const response = await this.api.post('/familias/', data);
    return response.data;
  }

  async updateFamily(id: number, data: any) {
    const response = await this.api.patch(`/familias/${id}/`, data);
    return response.data;
  }

  // Member endpoints
  async getMembers(familyId?: number) {
    const params = familyId ? { familia: familyId } : undefined;
    const response = await this.api.get('/membros/', { params });
    return response.data;
  }

  async getMember(id: number) {
    const response = await this.api.get(`/membros/${id}/`);
    return response.data;
  }

  async createMember(data: any) {
    const formData = new FormData();
    
    // Append all fields to form data
    Object.keys(data).forEach(key => {
      if (data[key] !== undefined && data[key] !== null) {
        formData.append(key, data[key]);
      }
    });

    const response = await this.api.post('/membros/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  async updateMember(id: number, data: any) {
    const formData = new FormData();
    
    // Append all fields to form data
    Object.keys(data).forEach(key => {
      if (data[key] !== undefined && data[key] !== null) {
        formData.append(key, data[key]);
      }
    });

    const response = await this.api.patch(`/membros/${id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  // Class endpoints
  async getClasses() {
    const response = await this.api.get('/turmas/');
    return response.data;
  }

  // Attendance endpoints
  async getAttendances(params?: Record<string, any>) {
    const response = await this.api.get('/presencas/', { params });
    return response.data;
  }

  async updateAttendance(id: number, data: { presente: boolean; observacoes?: string }) {
    const response = await this.api.patch(`/presencas/${id}/`, data);
    return response.data;
  }

  // Basket delivery endpoints
  async getBasketDeliveries(params?: Record<string, any>) {
    const response = await this.api.get('/entregas-cestas/', { params });
    return response.data;
  }

  async createBasketDelivery(data: any) {
    const response = await this.api.post('/entregas-cestas/', data);
    return response.data;
  }

  // Dashboard endpoints
  async getDashboardStats() {
    const response = await this.api.get('/dashboard/stats/');
    return response.data;
  }
}

export const api = new ApiService();
