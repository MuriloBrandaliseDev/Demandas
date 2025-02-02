# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
import re
from .models import Demanda

Usuario = get_user_model()

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']
        

    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Usuário'})
        self.fields['email'].widget.attrs.update({'placeholder': 'E-mail'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Senha'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirme sua senha'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError("Um usuário com este nome de usuário já existe.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Já existe uma conta registrada com este e-mail.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError('A senha precisa ter pelo menos uma letra maiúscula.')
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError('A senha precisa ter pelo menos um número.')
        return password


class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # Autentica usando email ou username
        if '@' in username_or_email:
            try:
                user = Usuario.objects.get(email=username_or_email)
                username = user.username
            except Usuario.DoesNotExist:
                raise forms.ValidationError("Este e-mail não está registrado.")
        else:
            username = username_or_email

        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Usuário ou senha inválidos.")
        
        # Adiciona o usuário ao formulário
        self.cleaned_data['user'] = user
        return self.cleaned_data

    def get_user(self):
        return self.cleaned_data.get('user')
    

from django.contrib.auth.backends import ModelBackend
from .models import Usuario

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Autentica com email ou username
            user = Usuario.objects.get(email=username) if '@' in username else Usuario.objects.get(username=username)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Usuario.DoesNotExist:
            return None




class DemandaForm(forms.ModelForm):
    TAXA_URGENCIA_CHOICES = (
        (True, 'Sim'),
        (False, 'Não'),
    )

    data_demanda = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Data da Demanda"
    )

    taxa_urgencia = forms.TypedChoiceField(
        choices=TAXA_URGENCIA_CHOICES,
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True',
        label="Taxa de Urgência Necessária",
        required=False,
        initial=False,
    )

    class Meta:
        model = Demanda
        fields = [
            'nome_solicitante',
            'categoria',
            'taxa_urgencia',
            'titulo_projeto',
            'descricao',
            'status',
            'urgencia',
            'arquivo_adicional',
            'data_demanda',
        ]

        widgets = {
            'nome_solicitante': forms.TextInput(attrs={'placeholder': 'Nome do Solicitante'}),
            'categoria': forms.TextInput(attrs={'placeholder': 'Área do Projeto'}),
            'titulo_projeto': forms.TextInput(attrs={'placeholder': 'Título do Projeto'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Descreva seu projeto (desenvolvimento, manutenção, automação, etc.)'}),
            'status': forms.Select(attrs={'class': 'status-dropdown'}),
            'urgencia': forms.Select(attrs={'class': 'urgencia-dropdown'}),
            'data_demanda': forms.DateInput(attrs={'type': 'date'}),
            'arquivo_adicional': forms.ClearableFileInput(attrs={'class': 'arquivo-input'}),
        }

    def clean_arquivo_adicional(self):
        arquivo = self.cleaned_data.get('arquivo_adicional')
        if arquivo:
            if arquivo.size > 5 * 1024 * 1024:  # Limite de 5MB
                raise forms.ValidationError("O arquivo não pode exceder 5MB.")
            # Adicione validações adicionais, se necessário (tipo de arquivo, etc.)
        return arquivo


class SignatureForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Nome',
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu nome',
            'class': 'form-control'
        })
    )
    title = forms.CharField(
        max_length=100,
        label='Cargo',
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu cargo',
            'class': 'form-control'
        })
    )
    department = forms.CharField(
        max_length=100,
        label='Departamento',
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite o departamento',
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Digite seu e-mail',
            'class': 'form-control'
        })
    )
    phone = forms.CharField(
        max_length=20,
        label='Telefone',
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu telefone',
            'class': 'form-control'
        })
    )
    website = forms.URLField(
        label='Site',
        widget=forms.URLInput(attrs={
            'placeholder': 'Digite o URL do seu site',
            'class': 'form-control'
        })
    )
    profile_image = forms.ImageField(
        label='Imagem de Perfil',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file'
        })
    )




from .models import Membro

class MembroForm(forms.ModelForm):
    class Meta:
        model = Membro
        fields = ['nome', 'email', 'telefone', 'cargo']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'telefone': forms.NumberInput(attrs={'placeholder': 'Telefone (Opcional)'}),
            'cargo': forms.TextInput(attrs={'placeholder': 'Cargo (Opcional)'}),
        }


