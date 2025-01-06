# models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Usuario(AbstractUser):
    """
    Modelo personalizado de usuário que estende o AbstractUser do Django.
    Adiciona campos adicionais como telefone e endereço.
    """
    telefone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        verbose_name="Telefone"
    )
    endereco = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Endereço"
    )

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    # Adiciona related_name personalizados para evitar conflitos com o User padrão
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_groups',  # related_name personalizado
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_permissions',  # related_name personalizado
        blank=True
    )

    def __str__(self):
        return self.username

class Profile(models.Model):
    """
    Modelo de perfil relacionado ao usuário. Estende informações adicionais,
    como a imagem de perfil.
    """
    user = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE,
        related_name='profile',  # Facilita o acesso ao perfil a partir do usuário
        verbose_name="Usuário"
    )
    image = models.ImageField(
        default='default.jpg', 
        upload_to='profile_pics',
        verbose_name="Imagem de Perfil"
    )

    def __str__(self):
        return f'{self.user.username} Profile'

# Sinais para criar e salvar o perfil automaticamente quando um usuário é criado ou salvo
@receiver(post_save, sender=Usuario)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Usuario)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

from django.db import models
from datetime import datetime

class Demanda(models.Model):
    STATUS_CHOICES = [
        ('novo', 'Novo'),
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
        ('excluido', 'Excluído'),
    ]

    URGENCIA_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
    ]

    titulo_projeto = models.CharField(
        max_length=500, 
        verbose_name="Título do Projeto"
    )
    descricao = models.TextField(
        verbose_name="Descrição"
    )
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default='novo', 
        verbose_name="Status"
    )
    urgencia = models.CharField(
        max_length=50, 
        choices=URGENCIA_CHOICES, 
        verbose_name="Urgência"
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Data de Criação", 
        editable=False
    )
    data_demanda = models.DateField(
        verbose_name="Data da Demanda",
        default=datetime.now
    )
    nome_solicitante = models.CharField(
        max_length=255, 
        verbose_name="Nome do Solicitante"
    )
    categoria = models.CharField(
        max_length=255, 
        verbose_name="Categoria", 
        blank=True, 
        null=True
    )
    taxa_urgencia = models.BooleanField(
        default=False, 
        verbose_name="Taxa de Urgência Necessária"
    )
    arquivo_adicional = models.FileField(
        upload_to='demandas/arquivos/', 
        blank=True, 
        null=True, 
        verbose_name="Arquivo Adicional"
    )
    visivel = models.BooleanField(
        default=True, 
        verbose_name="Visível"
    )

    class Meta:
        verbose_name = "Demanda"
        verbose_name_plural = "Demandas"
        ordering = ['-data_criacao']

    def __str__(self):
        return f"{self.titulo_projeto} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if not self.data_demanda:
            self.data_demanda = self.data_criacao.date()
        super().save(*args, **kwargs)



from django.db import models

class Membro(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    cargo = models.CharField(max_length=50, blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)  # Novo campo para soft delete

    def __str__(self):
        return self.nome
    


