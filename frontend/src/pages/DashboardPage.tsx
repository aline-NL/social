import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/api';
import { DashboardStats } from '../types';
import {
  UserGroupIcon,
  HomeIcon,
  GiftIcon,
  ChartBarIcon,
  PlusIcon,
  UserPlusIcon,
  ClipboardDocumentCheckIcon,
} from '@heroicons/react/24/outline';

const stats = [
  { id: 1, name: 'Total de Famílias', value: '0', icon: HomeIcon },
  { id: 2, name: 'Membros Ativos', value: '0', icon: UserGroupIcon },
  { id: 3, name: 'Cestas Entregues (Mês)', value: '0', icon: GiftIcon },
  { id: 4, name: 'Famílias em Programas', value: '0', icon: ChartBarIcon },
];

const quickActions = [
  {
    name: 'Cadastrar Família',
    href: '/familias/novo',
    icon: PlusIcon,
    description: 'Adicionar uma nova família ao sistema',
    color: 'bg-indigo-500',
  },
  {
    name: 'Adicionar Membro',
    href: '/membros/novo',
    icon: UserPlusIcon,
    description: 'Cadastrar um novo membro em uma família',
    color: 'bg-green-500',
  },
  {
    name: 'Registrar Presença',
    href: '/presencas/novo',
    icon: ClipboardDocumentCheckIcon,
    description: 'Registrar presença em encontros',
    color: 'bg-yellow-500',
  },
  {
    name: 'Registrar Entrega',
    href: '/cestas/novo',
    icon: GiftIcon,
    description: 'Registrar entrega de cesta básica',
    color: 'bg-blue-500',
  },
];

export const DashboardPage = () => {
  const [statsData, setStatsData] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const data = await api.getDashboardStats();
        setStatsData(data);
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const displayStats = stats.map((stat, index) => ({
    ...stat,
    value: statsData
      ? index === 0
        ? statsData.total_familias.toString()
        : index === 1
        ? statsData.total_membros_ativos.toString()
        : index === 2
        ? statsData.cestas_entregues_mes.toString()
        : statsData.familias_programas_sociais.toString()
      : '0',
  }));

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      </div>
    );
  }


  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Bem-vindo(a), {user?.first_name}!</h1>
        <p className="mt-1 text-sm text-gray-500">
          Aqui está um resumo das atividades do sistema.
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {displayStats.map((stat) => (
          <div
            key={stat.id}
            className="relative overflow-hidden rounded-lg bg-white px-4 pt-5 pb-12 shadow sm:px-6 sm:pt-6"
          >
            <dt>
              <div className="absolute rounded-md bg-primary-500 p-3">
                <stat.icon className="h-6 w-6 text-white" aria-hidden="true" />
              </div>
              <p className="ml-16 truncate text-sm font-medium text-gray-500">
                {stat.name}
              </p>
            </dt>
            <dd className="ml-16 flex items-baseline pb-6 sm:pb-7">
              <p className="text-2xl font-semibold text-gray-900">
                {stat.value}
              </p>
            </dd>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="mt-8">
        <h2 className="text-lg font-medium text-gray-900">Ações Rápidas</h2>
        <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {quickActions.map((action) => (
            <Link
              key={action.name}
              to={action.href}
              className="relative flex items-center space-x-3 rounded-lg border border-gray-300 bg-white px-6 py-5 shadow-sm focus-within:ring-2 focus-within:ring-primary-500 focus-within:ring-offset-2 hover:border-gray-400"
            >
              <div className="flex-shrink-0">
                <div className={`h-10 w-10 rounded-md ${action.color} flex items-center justify-center`}>
                  <action.icon className="h-6 w-6 text-white" aria-hidden="true" />
                </div>
              </div>
              <div className="min-w-0 flex-1">
                <div className="focus:outline-none">
                  <span className="absolute inset-0" aria-hidden="true" />
                  <p className="text-sm font-medium text-gray-900">
                    {action.name}
                  </p>
                  <p className="truncate text-sm text-gray-500">
                    {action.description}
                  </p>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Recent Activity (Placeholder) */}
      <div className="mt-8">
        <h2 className="text-lg font-medium text-gray-900">Atividades Recentes</h2>
        <div className="mt-4 overflow-hidden bg-white shadow sm:rounded-md">
          <ul role="list" className="divide-y divide-gray-200">
            {[1, 2, 3].map((item) => (
              <li key={item}>
                <div className="px-4 py-4 sm:px-6">
                  <div className="flex items-center justify-between">
                    <p className="truncate text-sm font-medium text-primary-600">
                      Atividade {item}
                    </p>
                    <div className="ml-2 flex flex-shrink-0">
                      <p className="inline-flex rounded-full bg-green-100 px-2 text-xs font-semibold leading-5 text-green-800">
                        Completo
                      </p>
                    </div>
                  </div>
                  <div className="mt-2 sm:flex sm:justify-between">
                    <p className="text-sm text-gray-500">
                      Descrição da atividade recente realizada no sistema.
                    </p>
                    <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                      <p>Há {item} hora{item !== 1 ? 's' : ''}</p>
                    </div>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};
