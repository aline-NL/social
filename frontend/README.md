# Sistema de Atendimento Social

Frontend do Sistema de Atendimento Social desenvolvido com React, TypeScript, Vite e Tailwind CSS.

## Recursos

- **Autenticação** com diferentes níveis de acesso (Admin, Atendente, Visualizador)
- **Dashboard** com métricas importantes
- **Cadastro de Famílias** com endereço e informações de programas sociais
- **Gerenciamento de Membros** com fotos e informações detalhadas
- **Controle de Presença** em encontros e atividades
- **Registro de Entregas** de cestas básicas
- **Relatórios** e estatísticas

## Tecnologias

- [React](https://react.dev/) - Biblioteca JavaScript para interfaces de usuário
- [TypeScript](https://www.typescriptlang.org/) - Adiciona tipagem estática ao JavaScript
- [Vite](https://vitejs.dev/) - Ferramenta de build e desenvolvimento
- [Tailwind CSS](https://tailwindcss.com/) - Framework CSS utilitário
- [React Router](https://reactrouter.com/) - Roteamento no cliente
- [React Hook Form](https://react-hook-form.com/) - Gerenciamento de formulários
- [React Query](https://tanstack.com/query) - Gerenciamento de estado do servidor
- [Hero Icons](https://heroicons.com/) - Biblioteca de ícones

## Começando
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default tseslint.config({
  plugins: {
    // Add the react-x and react-dom plugins
    'react-x': reactX,
    'react-dom': reactDom,
  },
  rules: {
    // other rules...
    // Enable its recommended typescript rules
    ...reactX.configs['recommended-typescript'].rules,
    ...reactDom.configs.recommended.rules,
  },
})
```
