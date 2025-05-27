import { rest } from 'msw';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const handlers = [
  // Auth handlers
  rest.post(`${API_URL}/auth/login`, (req, res, ctx) => {
    const { email, password } = req.body as { email: string; password: string };

    // Mock de autenticação bem-sucedida
    if (email === 'admin@example.com' && password === 'password') {
      return res(
        ctx.delay(150),
        ctx.status(200),
        ctx.json({
          access_token: 'mock-access-token',
          refresh_token: 'mock-refresh-token',
          user: {
            id: 1,
            email: 'admin@example.com',
            name: 'Admin User',
            role: 'admin',
          },
        })
      );
    }

    // Mock de erro de autenticação
    return res(
      ctx.delay(150),
      ctx.status(401),
      ctx.json({
        message: 'Credenciais inválidas',
      })
    );
  }),

  // User profile
  rest.get(`${API_URL}/auth/me`, (req, res, ctx) => {
    const token = req.headers.get('Authorization')?.replace('Bearer ', '');

    if (token === 'mock-access-token') {
      return res(
        ctx.delay(150),
        ctx.status(200),
        ctx.json({
          id: 1,
          email: 'admin@example.com',
          name: 'Admin User',
          role: 'admin',
        })
      );
    }

    return res(
      ctx.delay(150),
      ctx.status(401),
      ctx.json({ message: 'Não autorizado' })
    );
  }),

  // Dashboard stats
  rest.get(`${API_URL}/dashboard/stats`, (req, res, ctx) => {
    return res(
      ctx.delay(150),
      ctx.status(200),
      ctx.json({
        totalFamilies: 124,
        totalMembers: 487,
        basketsDelivered: 98,
        socialPrograms: 5,
      })
    );
  }),

  // Families
  rest.get(`${API_URL}/families`, (req, res, ctx) => {
    return res(
      ctx.delay(150),
      ctx.status(200),
      ctx.json({
        data: Array(10).fill(0).map((_, i) => ({
          id: i + 1,
          responsibleName: `Família ${i + 1}`,
          responsibleNis: `123.45678.90-${i}`.padStart(15, '0'),
          responsibleCpf: `123.456.789-${i.toString().padStart(2, '0')}`,
          responsiblePhone: `(11) 98765-43${i.toString().padStart(2, '0')}`,
          address: `Rua Exemplo, ${i + 100} - Bairro Teste`,
          referencePoint: 'Próximo ao mercado',
          familyIncome: (1000 + i * 100).toFixed(2),
          createdAt: new Date(Date.now() - i * 86400000).toISOString(),
          updatedAt: new Date().toISOString(),
        })),
        meta: {
          total: 124,
          page: 1,
          perPage: 10,
          totalPages: 13,
        },
      })
    );
  }),

  // Members
  rest.get(`${API_URL}/families/:familyId/members`, (req, res, ctx) => {
    const { familyId } = req.params;
    
    return res(
      ctx.delay(150),
      ctx.status(200),
      ctx.json({
        data: Array(3).fill(0).map((_, i) => ({
          id: i + 1,
          familyId: Number(familyId),
          name: `Membro ${i + 1} da Família ${familyId}`,
          cpf: `123.456.789-${i.toString().padStart(2, '0')}`,
          birthDate: new Date(1990 + i, i % 12, (i + 1) % 28).toISOString(),
          gender: ['male', 'female', 'other'][i % 3],
          race: ['white', 'black', 'brown', 'yellow', 'indigenous'][i % 5],
          isResponsible: i === 0,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        })),
      })
    );
  }),
];
