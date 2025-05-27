// User types
export type UserRole = 'admin' | 'atendente' | 'visualizador';

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  tipo: UserRole;
  is_active: boolean;
  date_joined: string;
}

// Auth types
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface AuthResponse {
  user: User;
  token: string;
}

// Address types
export interface Endereco {
  id: number;
  logradouro: string;
  numero: string;
  complemento?: string;
  bairro: string;
  cidade: string;
  estado: string;
  cep: string;
}

// Family types
export interface Familia {
  id: number;
  nome?: string;
  endereco: Endereco;
  observacoes?: string;
  recebe_programas_sociais: boolean;
  programas_sociais?: string;
  data_cadastro: string;
  data_atualizacao: string;
}

// Family member types
export type Sexo = 'M' | 'F' | 'O';
export type TamanhoCamiseta = 'PP' | 'P' | 'M' | 'G' | 'GG' | 'XG' | 'XXG';

export interface MembroFamilia {
  id: number;
  nome_completo: string;
  data_nascimento: string;
  sexo: Sexo;
  numero_calcado?: number;
  tamanho_calca?: string;
  tamanho_camiseta?: TamanhoCamiseta;
  foto?: string;
  familia: number; // Family ID
  ativo: boolean;
  data_cadastro: string;
  data_atualizacao: string;
}

// Responsible person types
export interface Responsavel {
  id: number;
  nome_completo: string;
  cpf?: string;
  telefone: string;
  data_nascimento: string;
  sexo: Sexo;
  familia: number; // Family ID
  principal: boolean;
  data_cadastro: string;
  data_atualizacao: string;
}

// Class types
export interface Turma {
  id: number;
  nome: string;
  idade_minima: number;
  idade_maxima: number;
  ativo: boolean;
  descricao?: string;
}

// Meeting types
export interface Encontro {
  id: number;
  data: string;
  descricao?: string;
  ativo: boolean;
}

// Attendance types
export interface Presenca {
  id: number;
  membro: number; // Membro ID
  encontro: number; // Encontro ID
  presente: boolean;
  observacoes?: string;
  data_registro: string;
  usuario_registro: number; // User ID
}

// Basket delivery types
export interface EntregaCesta {
  id: number;
  familia: number; // Family ID
  data_entrega: string;
  observacoes?: string;
  usuario_registro: number; // User ID
  data_registro: string;
}

// System configuration types
export interface ConfiguracaoSistema {
  chave: string;
  valor: string;
  descricao?: string;
}

// Dashboard stats
export interface DashboardStats {
  total_familias: number;
  total_membros_ativos: number;
  cestas_entregues_mes: number;
  familias_programas_sociais: number;
}

// API response types
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
