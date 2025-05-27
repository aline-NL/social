import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';

// Use process.env for Jest compatibility
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

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
        const token = localStorage.getItem('token');
        if (token) {
          config.headers.Authorization = `Token ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async login(credentials: { email: string; password: string }) {
    const response = await this.api.post('/auth/login/', credentials);
    return response.data;
  }

  async getCurrentUser() {
    const response = await this.api.get('/auth/me/');
    return response.data;
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
