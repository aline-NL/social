/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** URL base da API */
  readonly VITE_API_URL: string;
  
  /** Habilitar recursos de análise (true/false) */
  readonly VITE_ENABLE_ANALYTICS: string;
  
  /** Chave para armazenar o token de autenticação */
  readonly VITE_AUTH_TOKEN_KEY: string;
  
  /** Chave para armazenar o token de atualização */
  readonly VITE_REFRESH_TOKEN_KEY: string;
  
  /** Nome da aplicação */
  readonly VITE_APP_NAME: string;
  
  /** Versão da aplicação */
  readonly VITE_APP_VERSION: string;
  
  /** Descrição da aplicação */
  readonly VITE_APP_DESCRIPTION: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
