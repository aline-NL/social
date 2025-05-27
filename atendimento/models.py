from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
import os

def membro_foto_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/membros_fotos/<membro_id>/<filename>
    return os.path.join('membros_fotos', str(instance.id), filename)

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('tipo', 'admin')
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractUser):
    TIPO_CHOICES = [
        ('admin', 'Administrador'),
        ('atendente', 'Atendente'),
        ('visualizador', 'Visualizador'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='visualizador')
    email = models.EmailField(_('email address'), unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UsuarioManager()
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_tipo_display()})"
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

class Endereco(models.Model):
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)
    
    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}"
    
    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

class Familia(models.Model):
    nome = models.CharField(max_length=200, blank=True, null=True, help_text="Nome de referência para a família (opcional)")
    endereco = models.OneToOneField(Endereco, on_delete=models.PROTECT, related_name='familia')
    observacoes = models.TextField(blank=True, null=True)
    recebe_programas_sociais = models.BooleanField(default=False)
    programas_sociais = models.TextField(blank=True, null=True, help_text="Lista de programas sociais que a família recebe")
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nome or f"Família #{self.id}"
    
    class Meta:
        verbose_name = 'Família'
        verbose_name_plural = 'Famílias'
        ordering = ['nome', 'data_cadastro']

class Responsavel(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    
    nome_completo = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, blank=True, null=True, help_text="Formato: 000.000.000-00")
    telefone = models.CharField(max_length=20)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name='responsaveis')
    principal = models.BooleanField(default=False)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    def clean(self):
        # Garante que haja apenas um responsável principal por família
        if self.principal and self.familia.responsaveis.filter(principal=True).exclude(id=self.id).exists():
            raise ValidationError('Já existe um responsável principal cadastrado para esta família.')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nome_completo} ({'Principal' if self.principal else 'Secundário'}) - {self.familia}"
    
    class Meta:
        verbose_name = 'Responsável'
        verbose_name_plural = 'Responsáveis'
        ordering = ['-principal', 'nome_completo']

class MembroFamilia(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    
    TAMANHO_CAMISETA_CHOICES = [
        ('PP', 'PP'),
        ('P', 'P'),
        ('M', 'M'),
        ('G', 'G'),
        ('GG', 'GG'),
        ('XG', 'XG'),
        ('XXG', 'XXG'),
    ]
    
    nome_completo = models.CharField(max_length=200)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    numero_calcado = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(18), MaxValueValidator(50)])
    tamanho_calca = models.CharField(max_length=10, blank=True, null=True, help_text="Ex: 38, 40, 42, P, M, G")
    tamanho_camiseta = models.CharField(max_length=3, choices=TAMANHO_CAMISETA_CHOICES, blank=True, null=True)
    foto = models.ImageField(upload_to=membro_foto_upload_path, blank=True, null=True)
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name='membros')
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    @property
    def idade(self):
        today = timezone.now().date()
        return today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))
    
    def __str__(self):
        return f"{self.nome_completo} ({self.idade} anos) - {self.familia}"
    
    class Meta:
        verbose_name = 'Membro da Família'
        verbose_name_plural = 'Membros da Família'
        ordering = ['nome_completo']

class Turma(models.Model):
    nome = models.CharField(max_length=100, help_text="Ex: 3 a 5 anos, 6 a 8 anos, etc.")
    idade_minima = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)])
    idade_maxima = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    ativo = models.BooleanField(default=True)
    descricao = models.TextField(blank=True, null=True)
    
    def clean(self):
        if self.idade_minima >= self.idade_maxima:
            raise ValidationError('A idade mínima deve ser menor que a idade máxima.')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nome} ({self.idade_minima} a {self.idade_maxima} anos)"
    
    class Meta:
        ordering = ['idade_minima']

class Encontro(models.Model):
    data = models.DateField(unique=True)
    descricao = models.CharField(max_length=200, blank=True, null=True)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Encontro de {self.data.strftime('%d/%m/%Y')} - {self.descricao or ''}"
    
    class Meta:
        ordering = ['-data']
        verbose_name = 'Encontro'
        verbose_name_plural = 'Encontros'

class Presenca(models.Model):
    membro = models.ForeignKey(MembroFamilia, on_delete=models.CASCADE, related_name='presencas')
    encontro = models.ForeignKey(Encontro, on_delete=models.CASCADE, related_name='presencas')
    presente = models.BooleanField(default=True)
    observacoes = models.TextField(blank=True, null=True)
    data_registro = models.DateTimeField(auto_now_add=True)
    usuario_registro = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='presencas_registradas')
    
    class Meta:
        unique_together = ('membro', 'encontro')
        verbose_name = 'Presença'
        verbose_name_plural = 'Presenças'
    
    def __str__(self):
        status = "Presente" if self.presente else "Faltou"
        return f"{self.membro} - {self.encontro}: {status}"

class EntregaCesta(models.Model):
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name='entregas_cestas')
    data_entrega = models.DateField()
    observacoes = models.TextField(blank=True, null=True)
    usuario_registro = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='entregas_registradas')
    data_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('familia', 'data_entrega')
        verbose_name = 'Entrega de Cesta'
        verbose_name_plural = 'Entregas de Cestas'
        ordering = ['-data_entrega']
    
    def clean(self):
        # Verifica se já existe entrega para esta família neste mês/ano
        if EntregaCesta.objects.filter(
            familia=self.familia,
            data_entrega__year=self.data_entrega.year,
            data_entrega__month=self.data_entrega.month
        ).exclude(id=self.id).exists():
            raise ValidationError('Já existe uma entrega de cesta para esta família neste mês.')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Cesta para {self.familia} em {self.data_entrega.strftime('%d/%m/%Y')}"

class ConfiguracaoSistema(models.Model):
    chave = models.CharField(max_length=100, unique=True)
    valor = models.TextField()
    descricao = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.chave}: {self.valor}"
    
    class Meta:
        verbose_name = 'Configuração do Sistema'
        verbose_name_plural = 'Configurações do Sistema'
