from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views_auth import CustomTokenObtainPairView, CustomTokenRefreshView, UserProfileView

router = DefaultRouter()

# Register viewsets
router.register(r'enderecos', views.EnderecoViewSet)
router.register(r'familias', views.FamiliaViewSet)
router.register(r'responsaveis', views.ResponsavelViewSet)
router.register(r'membros', views.MembroFamiliaViewSet)
router.register(r'turmas', views.TurmaViewSet)
router.register(r'encontros', views.EncontroViewSet)
router.register(r'presencas', views.PresencaViewSet)
router.register(r'entregas-cestas', views.EntregaCestaViewSet, basename='entregacesta')
router.register(r'configuracoes', views.ConfiguracaoSistemaViewSet, basename='configuracao')

# URLs de autenticação
auth_urls = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserProfileView.as_view(), name='user_profile'),
]

# Additional URL patterns
urlpatterns = [
    # API Root
    path('', include(router.urls)),
    
    # Autenticação
    path('auth/', include(auth_urls)),
    
    # Relatórios
    path('relatorios/', views.RelatoriosViewSet.as_view({'get': 'list'}), name='relatorios-list'),
    path('relatorios/frequencia-membros/', 
         views.RelatoriosViewSet.as_view({'get': 'frequencia_membros'}), 
         name='relatorio-frequencia-membros'),
    path('relatorios/entregas-cestas/', 
         views.RelatoriosViewSet.as_view({'get': 'entregas_cestas'}), 
         name='relatorio-entregas-cestas'),
    path('relatorios/grade-roupas/', 
         views.RelatoriosViewSet.as_view({'get': 'grade_roupas'}), 
         name='relatorio-grade-roupas'),
    path('relatorios/programas-sociais/', 
         views.RelatoriosViewSet.as_view({'get': 'programas_sociais'}), 
         name='relatorio-programas-sociais'),
    
    # Endpoints adicionais
    path('entregas-cestas/resumo-mensal/', 
         views.EntregaCestaViewSet.as_view({'get': 'resumo_mensal'}), 
         name='entregas-cestas-resumo-mensal'),
]
