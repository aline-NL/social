from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import (
    Endereco, Familia, Responsavel, MembroFamilia, Turma, 
    Encontro, Presenca, EntregaCesta, ConfiguracaoSistema
)

User = get_user_model()

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'tipo', 'is_staff', 'is_active')
    list_filter = ('tipo', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('User Type'), {'fields': ('tipo',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'tipo'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('rua', 'numero', 'bairro', 'cidade', 'estado', 'cep')
    search_fields = ('rua', 'bairro', 'cidade', 'cep')
    list_filter = ('estado', 'cidade')

class ResponsavelInline(admin.StackedInline):
    model = Responsavel
    extra = 0
    fields = ('nome_completo', 'cpf', 'telefone', 'data_nascimento', 'sexo', 'principal')

class MembroFamiliaInline(admin.StackedInline):
    model = MembroFamilia
    extra = 0
    fields = ('nome_completo', 'data_nascimento', 'sexo', 'numero_calcado', 'tamanho_calca', 'tamanho_camiseta', 'ativo')
    readonly_fields = ('idade',)

@admin.register(Familia)
class FamiliaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco', 'recebe_programas_sociais', 'data_cadastro')
    list_filter = ('recebe_programas_sociais', 'data_cadastro')
    search_fields = ('nome', 'endereco__rua', 'endereco__bairro', 'endereco__cidade')
    inlines = [ResponsavelInline, MembroFamiliaInline]
    fieldsets = (
        (None, {
            'fields': ('nome', 'endereco', 'recebe_programas_sociais', 'programas_sociais', 'observacoes')
        }),
        ('Datas', {
            'fields': ('data_cadastro', 'data_atualizacao'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('data_cadastro', 'data_atualizacao')

@admin.register(Responsavel)
class ResponsavelAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'familia', 'principal', 'telefone', 'data_nascimento')
    list_filter = ('principal', 'sexo')
    search_fields = ('nome_completo', 'cpf', 'telefone', 'familia__nome')
    raw_id_fields = ('familia',)

@admin.register(MembroFamilia)
class MembroFamiliaAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'familia', 'idade', 'sexo', 'ativo')
    list_filter = ('sexo', 'ativo', 'tamanho_camiseta')
    search_fields = ('nome_completo', 'familia__nome')
    list_editable = ('ativo',)
    readonly_fields = ('idade', 'data_cadastro', 'data_atualizacao')
    fieldsets = (
        (None, {
            'fields': ('nome_completo', 'data_nascimento', 'sexo', 'familia', 'ativo')
        }),
        ('Medidas', {
            'fields': ('numero_calcado', 'tamanho_calca', 'tamanho_camiseta')
        }),
        ('Outros', {
            'fields': ('foto', 'data_cadastro', 'data_atualizacao')
        }),
    )

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'idade_minima', 'idade_maxima', 'ativo')
    list_editable = ('ativo',)
    search_fields = ('nome', 'descricao')

class PresencaInline(admin.TabularInline):
    model = Presenca
    extra = 0
    fields = ('membro', 'presente', 'observacoes')
    readonly_fields = ('data_registro', 'usuario_registro')

@admin.register(Encontro)
class EncontroAdmin(admin.ModelAdmin):
    list_display = ('data', 'descricao', 'ativo')
    list_filter = ('ativo', 'data')
    search_fields = ('descricao',)
    inlines = [PresencaInline]
    date_hierarchy = 'data'

@admin.register(Presenca)
class PresencaAdmin(admin.ModelAdmin):
    list_display = ('membro', 'encontro', 'presente', 'data_registro', 'usuario_registro')
    list_filter = ('presente', 'encontro__data')
    search_fields = ('membro__nome_completo', 'encontro__descricao')
    list_select_related = ('membro', 'encontro', 'usuario_registro')
    readonly_fields = ('data_registro', 'usuario_registro')

@admin.register(EntregaCesta)
class EntregaCestaAdmin(admin.ModelAdmin):
    list_display = ('familia', 'data_entrega', 'usuario_registro', 'data_registro')
    list_filter = ('data_entrega', 'usuario_registro')
    search_fields = ('familia__nome', 'observacoes')
    date_hierarchy = 'data_entrega'
    readonly_fields = ('data_registro', 'usuario_registro')

@admin.register(ConfiguracaoSistema)
class ConfiguracaoSistemaAdmin(admin.ModelAdmin):
    list_display = ('chave', 'valor', 'descricao')
    search_fields = ('chave', 'valor', 'descricao')
    list_editable = ('valor',)
