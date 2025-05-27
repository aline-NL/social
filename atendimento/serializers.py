from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Endereco, Familia, Responsavel, MembroFamilia, 
    Turma, Encontro, Presenca, EntregaCesta, ConfiguracaoSistema
)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'tipo', 'is_active']
        read_only_fields = ['id', 'is_active']

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'

class FamiliaSerializer(serializers.ModelSerializer):
    endereco = EnderecoSerializer()
    
    class Meta:
        model = Familia
        fields = '__all__'
        read_only_fields = ['data_cadastro', 'data_atualizacao']
    
    def create(self, validated_data):
        endereco_data = validated_data.pop('endereco')
        endereco = Endereco.objects.create(**endereco_data)
        familia = Familia.objects.create(endereco=endereco, **validated_data)
        return familia
    
    def update(self, instance, validated_data):
        endereco_data = validated_data.pop('endereco', None)
        if endereco_data:
            endereco_serializer = self.fields['endereco']
            endereco = instance.endereco
            endereco = endereco_serializer.update(endereco, endereco_data)
            instance.endereco = endereco
        return super().update(instance, validated_data)

class ResponsavelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsavel
        fields = '__all__'
        read_only_fields = ['data_cadastro', 'data_atualizacao']

class MembroFamiliaSerializer(serializers.ModelSerializer):
    idade = serializers.ReadOnlyField()
    
    class Meta:
        model = MembroFamilia
        fields = '__all__'
        read_only_fields = ['data_cadastro', 'data_atualizacao', 'idade']

class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = '__all__'

class EncontroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encontro
        fields = '__all__'

class PresencaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presenca
        fields = '__all__'
        read_only_fields = ['data_registro', 'usuario_registro']

class EntregaCestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntregaCesta
        fields = '__all__'
        read_only_fields = ['data_registro', 'usuario_registro']

class ConfiguracaoSistemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracaoSistema
        fields = '__all__'
