from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q, F, Sum, Case, When, IntegerField, Value, BooleanField, CharField
from django.db.models.functions import Concat
from django.utils import timezone
from datetime import timedelta

from .models import (
    Endereco, Familia, Responsavel, MembroFamilia, 
    Turma, Encontro, Presenca, EntregaCesta, ConfiguracaoSistema
)
from .serializers import *

# ViewSets
class EnderecoViewSet(viewsets.ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cidade', 'estado', 'bairro']
    search_fields = ['rua', 'bairro', 'cidade', 'cep']
    ordering_fields = ['cidade', 'bairro', 'rua']

class FamiliaViewSet(viewsets.ModelViewSet):
    queryset = Familia.objects.all()
    serializer_class = FamiliaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['recebe_programas_sociais']
    search_fields = ['nome', 'endereco__rua', 'endereco__bairro', 'endereco__cidade']
    ordering_fields = ['nome', 'data_cadastro']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro para membros ativos
        membros_ativos = self.request.query_params.get('membros_ativos', None)
        if membros_ativos is not None:
            queryset = queryset.filter(membros__ativo=True).distinct()
        
        # Filtro por programa social
        programa_social = self.request.query_params.get('programa_social', None)
        if programa_social:
            queryset = queryset.filter(programas_sociais__icontains=programa_social)
            
        return queryset
    
    @action(detail=True, methods=['get'])
    def membros(self, request, pk=None):
        familia = self.get_object()
        membros = familia.membros.all()
        serializer = MembroFamiliaSerializer(membros, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def responsaveis(self, request, pk=None):
        familia = self.get_object()
        responsaveis = familia.responsaveis.all()
        serializer = ResponsavelSerializer(responsaveis, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def entregas_cestas(self, request, pk=None):
        familia = self.get_object()
        entregas = familia.entregas_cestas.all()
        serializer = EntregaCestaSerializer(entregas, many=True)
        return Response(serializer.data)

class ResponsavelViewSet(viewsets.ModelViewSet):
    queryset = Responsavel.objects.all()
    serializer_class = ResponsavelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['principal', 'sexo']
    search_fields = ['nome_completo', 'cpf', 'telefone', 'familia__nome']
    ordering_fields = ['nome_completo', 'data_nascimento']

class MembroFamiliaViewSet(viewsets.ModelViewSet):
    queryset = MembroFamilia.objects.all()
    serializer_class = MembroFamiliaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sexo', 'ativo', 'tamanho_camiseta']
    search_fields = ['nome_completo', 'familia__nome']
    ordering_fields = ['nome_completo', 'data_nascimento']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por faixa etária
        idade_min = self.request.query_params.get('idade_min', None)
        idade_max = self.request.query_params.get('idade_max', None)
        
        if idade_min is not None or idade_max is not None:
            today = timezone.now().date()
            
            if idade_min is not None:
                min_date = today.replace(year=today.year - int(idade_min) - 1)
                queryset = queryset.filter(data_nascimento__lte=min_date)
                
            if idade_max is not None:
                max_date = today.replace(year=today.year - int(idade_max) - 1)
                queryset = queryset.filter(data_nascimento__gte=max_date)
        
        return queryset

class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['idade_minima', 'nome']
    
    @action(detail=True, methods=['get'])
    def membros(self, request, pk=None):
        turma = self.get_object()
        hoje = timezone.now().date()
        
        # Calcula a data de nascimento mínima e máxima para a turma
        data_nasc_min = hoje.replace(year=hoje.year - turma.idade_maxima - 1)
        data_nasc_max = hoje.replace(year=hoje.year - turma.idade_minima)
        
        membros = MembroFamilia.objects.filter(
            data_nascimento__gte=data_nasc_min,
            data_nascimento__lte=data_nasc_max,
            ativo=True
        )
        
        # Anota cada membro com sua idade
        membros = membros.annotate(
            idade=hoje.year - F('data_nascimento__year') - 
                  Case(
                      When(
                          data_nascimento__month__gt=hoje.month,
                          then=Value(1)
                      ),
                      When(
                          data_nascimento__month=hoje.month,
                          data_nascimento__day__gt=hoje.day,
                          then=Value(1)
                      ),
                      default=Value(0),
                      output_field=IntegerField()
                  )
        )
        
        serializer = MembroFamiliaSerializer(membros, many=True)
        return Response(serializer.data)

class EncontroViewSet(viewsets.ModelViewSet):
    queryset = Encontro.objects.all()
    serializer_class = EncontroSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['descricao']
    ordering_fields = ['-data', 'descricao']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por data
        data_inicio = self.request.query_params.get('data_inicio', None)
        data_fim = self.request.query_params.get('data_fim', None)
        
        if data_inicio:
            queryset = queryset.filter(data__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data__lte=data_fim)
            
        return queryset
    
    @action(detail=True, methods=['get'])
    def presencas(self, request, pk=None):
        encontro = self.get_object()
        presencas = encontro.presencas.all()
        serializer = PresencaSerializer(presencas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def registrar_presencas(self, request, pk=None):
        encontro = self.get_object()
        presencas_data = request.data.get('presencas', [])
        
        # Validação básica
        if not isinstance(presencas_data, list):
            return Response(
                {'error': 'Dados de presenças devem ser uma lista'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Processa cada registro de presença
        resultados = []
        for presenca_data in presencas_data:
            membro_id = presenca_data.get('membro_id')
            presente = presenca_data.get('presente', False)
            observacoes = presenca_data.get('observacoes', '')
            
            try:
                membro = MembroFamilia.objects.get(id=membro_id, ativo=True)
                
                # Atualiza ou cria o registro de presença
                presenca, created = Presenca.objects.update_or_create(
                    membro=membro,
                    encontro=encontro,
                    defaults={
                        'presente': presente,
                        'observacoes': observacoes,
                        'usuario_registro': request.user
                    }
                )
                
                resultados.append({
                    'membro_id': membro_id,
                    'status': 'created' if created else 'updated',
                    'presenca_id': presenca.id
                })
                
            except MembroFamilia.DoesNotExist:
                resultados.append({
                    'membro_id': membro_id,
                    'status': 'error',
                    'error': 'Membro não encontrado ou inativo'
                })
        
        return Response({
            'encontro_id': encontro.id,
            'data': encontro.data,
            'resultados': resultados
        })

class PresencaViewSet(viewsets.ModelViewSet):
    queryset = Presenca.objects.all()
    serializer_class = PresencaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['presente', 'membro', 'encontro']
    search_fields = ['membro__nome_completo', 'encontro__descricao', 'observacoes']
    ordering_fields = ['-data_registro', '-encontro__data']
    
    def perform_create(self, serializer):
        serializer.save(usuario_registro=self.request.user)

class EntregaCestaViewSet(viewsets.ModelViewSet):
    queryset = EntregaCesta.objects.all()
    serializer_class = EntregaCestaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['familia']
    search_fields = ['familia__nome', 'observacoes']
    ordering_fields = ['-data_entrega', '-data_registro']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por período
        data_inicio = self.request.query_params.get('data_inicio', None)
        data_fim = self.request.query_params.get('data_fim', None)
        
        if data_inicio:
            queryset = queryset.filter(data_entrega__gte=data_inicio)
        if data_fim:
            # Adiciona 1 dia para incluir o dia final
            data_fim_obj = timezone.datetime.strptime(data_fim, '%Y-%m-%d').date()
            queryset = queryset.filter(data_entrega__lte=data_fim_obj + timedelta(days=1))
            
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(usuario_registro=self.request.user)
    
    @action(detail=False, methods=['get'])
    def resumo_mensal(self, request):
        # Agrupa as entregas por mês/ano
        resumo = EntregaCesta.objects.extra({
            'mes_ano': "to_char(data_entrega, 'MM/YYYY')"
        }).values('mes_ano').annotate(
            total=Count('id'),
            mes=Min('data_entrega__month'),
            ano=Min('data_entrega__year')
        ).order_by('-ano', '-mes')
        
        return Response(resumo)

class ConfiguracaoSistemaViewSet(viewsets.ModelViewSet):
    queryset = ConfiguracaoSistema.objects.all()
    serializer_class = ConfiguracaoSistemaSerializer
    permission_classes = [IsAdminUser]  # Apenas administradores podem modificar
    filter_backends = [filters.SearchFilter]
    search_fields = ['chave', 'descricao']
    
    def get_permissions(self):
        # Permite leitura para usuários autenticados
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()
    
    def get_object(self):
        # Permite buscar por chave ou ID
        if 'pk' in self.kwargs and not self.kwargs['pk'].isdigit():
            return self.get_queryset().get(chave=self.kwargs['pk'])
        return super().get_object()

# Views para relatórios e dashboards
class RelatoriosViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        # Lista de relatórios disponíveis
        relatorios = [
            {
                'nome': 'frequencia_membros',
                'descricao': 'Frequência de membros por período',
                'parametros': [
                    {'nome': 'data_inicio', 'tipo': 'date', 'obrigatorio': True},
                    {'nome': 'data_fim', 'tipo': 'date', 'obrigatorio': True},
                    {'nome': 'membro_id', 'tipo': 'integer', 'obrigatorio': False},
                    {'nome': 'familia_id', 'tipo': 'integer', 'obrigatorio': False},
                ]
            },
            {
                'nome': 'entregas_cestas',
                'descricao': 'Entregas de cestas por período',
                'parametros': [
                    {'nome': 'data_inicio', 'tipo': 'date', 'obrigatorio': True},
                    {'nome': 'data_fim', 'tipo': 'date', 'obrigatorio': True},
                ]
            },
            {
                'nome': 'grade_roupas',
                'descricao': 'Grade de roupas e calçados',
                'parametros': []
            },
            {
                'nome': 'programas_sociais',
                'descricao': 'Famílias por programa social',
                'parametros': []
            }
        ]
        return Response(relatorios)
    
    @action(detail=False, methods=['get'])
    def frequencia_membros(self, request):
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        membro_id = request.query_params.get('membro_id')
        familia_id = request.query_params.get('familia_id')
        
        if not data_inicio or not data_fim:
            return Response(
                {'error': 'Os parâmetros data_inicio e data_fim são obrigatórios'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filtra os encontros no período
        encontros = Encontro.objects.filter(
            data__gte=data_inicio,
            data__lte=data_fim,
            ativo=True
        ).order_by('data')
        
        # Filtra os membros ativos
        membros = MembroFamilia.objects.filter(ativo=True)
        if membro_id:
            membros = membros.filter(id=membro_id)
        if familia_id:
            membros = membros.filter(familia_id=familia_id)
        
        # Prepara os dados para o relatório
        resultado = []
        
        for membro in membros:
            # Conta presenças e faltas
            presencas = Presenca.objects.filter(
                membro=membro,
                encontro__in=encontros
            ).select_related('encontro')
            
            total_encontros = encontros.count()
            total_presente = presencas.filter(presente=True).count()
            total_faltas = presencas.filter(presente=False).count()
            
            # Calcula a frequência percentual
            frequencia_percentual = 0
            if total_encontros > 0:
                frequencia_percentual = (total_presente / total_encontros) * 100
            
            # Detalhes das presenças
            detalhes = []
            for encontro in encontros:
                presenca = presencas.filter(encontro=encontro).first()
                detalhes.append({
                    'data': encontro.data,
                    'presente': presenca.presente if presenca else False,
                    'observacoes': presenca.observacoes if presenca else ''
                })
            
            resultado.append({
                'membro_id': membro.id,
                'membro_nome': membro.nome_completo,
                'familia_id': membro.familia.id,
                'familia_nome': str(membro.familia),
                'total_encontros': total_encontros,
                'total_presente': total_presente,
                'total_faltas': total_faltas,
                'frequencia_percentual': round(frequencia_percentual, 2),
                'detalhes': detalhes
            })
        
        return Response(resultado)
    
    @action(detail=False, methods=['get'])
    def entregas_cestas(self, request):
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        
        if not data_inicio or not data_fim:
            return Response(
                {'error': 'Os parâmetros data_inicio e data_fim são obrigatórios'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filtra as entregas no período
        entregas = EntregaCesta.objects.filter(
            data_entrega__gte=data_inicio,
            data_entrega__lte=data_fim
        ).select_related('familia', 'usuario_registro')
        
        # Agrupa por mês/ano
        resultado = {}
        
        for entrega in entregas:
            mes_ano = entrega.data_entrega.strftime('%m/%Y')
            
            if mes_ano not in resultado:
                resultado[mes_ano] = {
                    'mes_ano': mes_ano,
                    'mes': entrega.data_entrega.month,
                    'ano': entrega.data_entrega.year,
                    'total_entregas': 0,
                    'familias': []
                }
            
            resultado[mes_ano]['total_entregas'] += 1
            resultado[mes_ano]['familias'].append({
                'familia_id': entrega.familia.id,
                'familia_nome': str(entrega.familia),
                'data_entrega': entrega.data_entrega,
                'usuario_registro': entrega.usuario_registro.get_full_name() if entrega.usuario_registro else 'Sistema',
                'observacoes': entrega.observacoes
            })
        
        # Ordena por data (mais recente primeiro)
        resultado_ordenado = sorted(
            resultado.values(),
            key=lambda x: (x['ano'], x['mes']),
            reverse=True
        )
        
        return Response(resultado_ordenado)
    
    @action(detail=False, methods=['get'])
    def grade_roupas(self, request):
        # Agrupa os membros por tamanho de roupa e calçado
        membros = MembroFamilia.objects.filter(ativo=True)
        
        # Tamanhos de camiseta
        tamanhos_camiseta = dict(MembroFamilia.TAMANHO_CAMISETA_CHOICES)
        contagem_camisetas = membros.filter(tamanho_camiseta__isnull=False)\
            .values('tamanho_camiseta')\
            .annotate(total=Count('id'))\
            .order_by('tamanho_camiseta')
        
        # Tamanhos de calça/bermuda
        contagem_calcas = membros.filter(tamanho_calca__isnull=False)\
            .values('tamanho_calca')\
            .annotate(total=Count('id'))\
            .order_by('tamanho_calca')
        
        # Números de calçado
        contagem_calcados = membros.filter(numero_calcado__isnull=False)\
            .values('numero_calcado')\
            .annotate(total=Count('id'))\
            .order_by('numero_calcado')
        
        # Formata os resultados
        resultado = {
            'camisetas': [
                {'tamanho': tamanhos_camiseta.get(item['tamanho_camiseta'], item['tamanho_camiseta']), 
                 'total': item['total']}
                for item in contagem_camisetas
            ],
            'calcas': [
                {'tamanho': item['tamanho_calca'], 'total': item['total']}
                for item in contagem_calcas
            ],
            'calcados': [
                {'numero': item['numero_calcado'], 'total': item['total']}
                for item in contagem_calcados
            ]
        }
        
        return Response(resultado)
    
    @action(detail=False, methods=['get'])
    def programas_sociais(self, request):
        # Conta famílias por programa social
        familias = Familia.objects.filter(recebe_programas_sociais=True)
        
        # Extrai programas sociais únicos
        programas = {}
        
        for familia in familias:
            if familia.programas_sociais:
                # Divide por vírgula, ponto-e-vírgula ou quebra de linha
                programas_familia = [p.strip() for p in familia.programas_sociais.replace(';', ',').replace('\n', ',').split(',') if p.strip()]
                
                for programa in programas_familia:
                    if programa not in programas:
                        programas[programa] = 0
                    programas[programa] += 1
        
        # Ordena por quantidade (maior primeiro)
        programas_ordenados = [
            {'programa': programa, 'total_familias': total}
            for programa, total in sorted(programas.items(), key=lambda x: x[1], reverse=True)
        ]
        
        # Total de famílias que recebem algum programa
        total_familias = familias.count()
        
        return Response({
            'total_familias': total_familias,
            'total_programas': len(programas_ordenados),
            'programas': programas_ordenados
        })
