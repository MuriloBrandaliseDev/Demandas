# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Membro
import logging
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_protect
from .forms import (
    RegistroForm,
    EmailOrUsernameAuthenticationForm,
    DemandaForm,
    SignatureForm
)
from .models import Demanda
import logging

logger = logging.getLogger(__name__)

# ======================================================
# 1. Registro de Usuário
# ======================================================

@csrf_protect
def registro(request):
    """
    View para registro de novos usuários.
    """
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Conta criada com sucesso!")
                return redirect('dashboard')  # Redireciona para o dashboard após o registro
        else:
            # Adiciona mensagens de erro específicas
            if form.errors.get('username'):
                messages.error(request, "Nome de usuário já existe.")
            elif form.errors.get('email'):
                messages.error(request, "Já existe uma conta com este e-mail.")
            else:
                messages.error(request, "Erro no registro. Verifique os campos e tente novamente.")
    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {'form': form})

# ======================================================
# 2. Login de Usuário
# ======================================================

@csrf_protect
def login_view(request):
    """
    View para login de usuários usando e-mail ou nome de usuário.
    """
    show_options = request.GET.get('show_options', 'false') == 'true'
    if request.method == 'POST':
        form = EmailOrUsernameAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            login(request, user)
            return redirect('dashboard')  # Redireciona para o dashboard após o login
        else:
            messages.error(request, "Formulário inválido. Verifique os campos.")
    else:
        form = EmailOrUsernameAuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form, 'show_options': show_options})

# ======================================================
# 3. Logout de Usuário
# ======================================================

def logout_view(request):
    """
    View para logout de usuários.
    """
    logout(request)
    messages.success(request, "Você foi desconectado com sucesso.")
    return redirect('login')

# ======================================================
# 4. Dashboard (AJAX)
# ======================================================

def dashboard(request):
    """
    View para exibir o dashboard via AJAX.
    """
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('conteudos/dashboard.html', request=request)
        return JsonResponse({'html': html})
    else:
        return render(request, 'base.html')
    

# usuarios/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Demanda
from datetime import datetime
import calendar

def calendario(request):
    """
    View para exibir o calendário com demandas cadastradas.
    """
    if request.headers.get('x-requested_with') == 'XMLHttpRequest':
        ano = datetime.now().year
        
        # Lista de nomes dos meses em Português Brasileiro
        meses_pt_br = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]
        
        # Buscar demandas do ano atual que estão visíveis
        demandas = Demanda.objects.filter(data_demanda__year=ano, visivel=True)
        
        # Organizar demandas por mês e dia
        demandas_por_mes_dia = {}
        for demanda in demandas:
            mes = demanda.data_demanda.month
            dia = demanda.data_demanda.day
            if mes not in demandas_por_mes_dia:
                demandas_por_mes_dia[mes] = {}
            if dia not in demandas_por_mes_dia[mes]:
                demandas_por_mes_dia[mes][dia] = []
            demandas_por_mes_dia[mes][dia].append(demanda)
        
        # Preparar lista de meses com nome e dias
        meses = []
        for mes_num in range(1, 13):
            nome_mes = meses_pt_br[mes_num - 1]
            dias_no_mes = calendar.monthrange(ano, mes_num)[1]
            dias = []
            for dia in range(1, dias_no_mes + 1):
                demandas_do_dia = demandas_por_mes_dia.get(mes_num, {}).get(dia, [])
                dias.append({
                    'dia': dia,
                    'demandas': demandas_do_dia
                })
            meses.append({
                'nome': nome_mes,
                'dias': dias
            })
        
        # Renderizar o template com os dados
        html = render_to_string('conteudos/calendario.html', {
            'meses': meses,
            'ano': ano
        }, request=request)
        
        return JsonResponse({'html': html})
    else:
        return render(request, 'base.html')


# ======================================================
# 5. Relatórios (CRUD de Demandas via AJAX)
# ======================================================

def relatorios(request):
    """
    View para criar e exibir demandas via AJAX.
    """
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        form = DemandaForm(request.POST, request.FILES)
        if form.is_valid():
            demanda = form.save()
            return JsonResponse({'success': True, 'message': 'Demanda cadastrada com sucesso!'})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    
    elif request.headers.get("x-requested-with") == "XMLHttpRequest":
        form = DemandaForm()
        html = render_to_string("conteudos/relatorios.html", {"form": form}, request=request)
        return JsonResponse({"html": html})
    else:
        return JsonResponse({"success": False, "message": "Requisição inválida"})

# ======================================================
# 6. Configurações (Listagem de Demandas via AJAX)
# ======================================================

def configuracoes(request):
    """
    View para listar demandas visíveis via AJAX.
    """
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        try:
            demandas = Demanda.objects.filter(visivel=True)
            html = render_to_string("conteudos/configuracoes.html", {"demandas": demandas}, request=request)
            return JsonResponse({"html": html})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    else:
        return JsonResponse({"success": False, "message": "Requisição inválida"})

# ======================================================
# 7. Concluir Demanda
# ======================================================

@csrf_protect
def concluir_demanda(request, demanda_id):
    """
    View para concluir uma demanda via AJAX.
    """
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        demanda = get_object_or_404(Demanda, id=demanda_id)
        demanda.status = 'concluido'
        demanda.visivel = False
        demanda.save()
        return JsonResponse({'success': True, 'message': 'Demanda concluída com sucesso!'})
    return JsonResponse({"success": False, "message": "Método inválido."})



# ======================================================
# 8. Excluir Demanda
# ======================================================

@csrf_protect
def excluir_demanda(request, demanda_id):
    """
    View para excluir uma demanda via AJAX.
    """
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        demanda = get_object_or_404(Demanda, id=demanda_id)
        demanda.status = 'excluido'
        demanda.visivel = False
        demanda.save()
        return JsonResponse({"success": True, "message": "Demanda excluída com sucesso!"})
    else:
        return JsonResponse({"success": False, "message": "Método não permitido."})
    

# ======================================================
# 9. Editar Demanda
# ======================================================

@csrf_protect
def editar_demanda(request, demanda_id):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        demanda = get_object_or_404(Demanda, id=demanda_id)
        try:
            titulo = request.POST.get("titulo_projeto")
            descricao = request.POST.get("descricao")
            status = request.POST.get("status")
            urgencia = request.POST.get("urgencia")
            nome_solicitante = request.POST.get("nome_solicitante")
            categoria = request.POST.get("categoria")
            taxa_urgencia = request.POST.get("taxa_urgencia")  # Certifique-se de que este campo está presente no formulário

            # Atualiza os campos da demanda
            demanda.titulo_projeto = titulo
            demanda.descricao = descricao
            demanda.status = status
            demanda.urgencia = urgencia
            demanda.nome_solicitante = nome_solicitante
            demanda.categoria = categoria
            demanda.taxa_urgencia = True if taxa_urgencia == "Sim" else False

            # Atualiza o arquivo adicional se houver
            if request.FILES.get("arquivo_adicional"):
                demanda.arquivo_adicional = request.FILES.get("arquivo_adicional")

            demanda.save()

            response_data = {
                "success": True,
                "message": "Demanda atualizada com sucesso!",
                "status_display": demanda.get_status_display(),
                "data_criacao": demanda.data_criacao.strftime("%d/%m/%Y %H:%M"),
                "urgencia_display": demanda.get_urgencia_display(),
                "taxa_urgencia": "Sim" if demanda.taxa_urgencia else "Não",
                "categoria": demanda.categoria,
                "nome_solicitante": demanda.nome_solicitante,
                "titulo_projeto": demanda.titulo_projeto,
                "descricao": demanda.descricao,
            }

            if demanda.arquivo_adicional:
                response_data["arquivo_adicional_url"] = demanda.arquivo_adicional.url

            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Método inválido."})


# ======================================================
# 10. Equipe (Conteúdo via AJAX)
# ======================================================




logger = logging.getLogger(__name__)

def equipe(request):
    """
    View para exibir a página da equipe via AJAX.
    """
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            membros = Membro.objects.filter(ativo=True).order_by('nome')  # Filtra apenas membros ativos
            html = render_to_string('conteudos/equipe.html', {'membros': membros}, request=request)
            return JsonResponse({'html': html})
        except Exception as e:
            logger.error(f"Erro ao carregar equipe: {e}")
            return JsonResponse({'error': 'Erro ao carregar a equipe.'}, status=500)
    else:
        return render(request, 'base.html')
    

from django.views.decorators.http import require_POST 

@csrf_protect
@require_POST
def excluir_membro(request, membro_id):
    if request.method == 'POST':
        try:
            membro = Membro.objects.get(id=membro_id)
            membro.ativo = False  # Marca o membro como inativo
            membro.save()
            logger.info(f"Membro inativado: {membro}")
            return JsonResponse({'success': True, 'message': 'Membro excluído com sucesso!'}, status=200)
        except Membro.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Membro não encontrado.'}, status=404)
        except Exception as e:
            logger.error(f"Erro ao inativar membro: {e}")
            return JsonResponse({'success': False, 'message': f'Erro ao inativar membro: {str(e)}'}, status=500)
    return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)


logger = logging.getLogger(__name__)


@csrf_protect
def cadastrar_membro(request):
    if request.method == 'POST':
        try:
            # Captura os dados enviados
            nome = request.POST.get('nome')
            email = request.POST.get('email')
            telefone = request.POST.get('telefone', '')
            cargo = request.POST.get('cargo', '')

            # Validações básicas
            if not nome or not email:
                return JsonResponse({'error': 'Nome e email são obrigatórios!'}, status=400)

            # Verifica se o email já existe
            if Membro.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email já cadastrado!'}, status=400)

            # Cria e salva o novo membro
            novo_membro = Membro(nome=nome, email=email, telefone=telefone, cargo=cargo)
            novo_membro.save()

            logger.info(f"Membro cadastrado: {novo_membro}")
            return JsonResponse({'message': 'Membro cadastrado com sucesso!'}, status=201)
        except Exception as e:
            logger.error(f"Erro ao cadastrar membro: {e}")
            return JsonResponse({'error': 'Erro ao salvar no banco de dados'}, status=500)
    return JsonResponse({'error': 'Método não permitido'}, status=405)    
    


@csrf_protect
def editar_membro(request, membro_id):
    """
    View para editar um membro existente.
    """
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        membro = get_object_or_404(Membro, id=membro_id)
        try:
            # Captura os dados enviados
            nome = request.POST.get('nome').strip()
            email = request.POST.get('email').strip()
            telefone = request.POST.get('telefone', '').strip()
            cargo = request.POST.get('cargo', '').strip()
    
            # Validações básicas
            if not nome or not email:
                return JsonResponse({'success': False, 'message': 'Nome e Email são obrigatórios.'}, status=400)
    
            # Verifica se o email já está sendo usado por outro membro
            if Membro.objects.filter(email=email).exclude(id=membro_id).exists():
                return JsonResponse({'success': False, 'message': 'Email já está sendo utilizado por outro membro.'}, status=400)
    
            # Atualiza os campos do membro
            membro.nome = nome
            membro.email = email
            membro.telefone = telefone if telefone else None
            membro.cargo = cargo if cargo else None
            membro.save()
    
            return JsonResponse({'success': True, 'message': 'Membro atualizado com sucesso!'}, status=200)
        except Exception as e:
            logger.error(f"Erro ao editar membro: {e}")
            return JsonResponse({'success': False, 'message': 'Erro ao atualizar o membro.'}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)


# ======================================================
# 11. Histórico de Demandas
# ======================================================

def historico_demandas(request):
    """
    View para exibir o histórico de demandas concluídas ou excluídas via AJAX.
    """
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        demandas = Demanda.objects.filter(status__in=['concluido', 'excluido']).order_by('-data_criacao')
        html = render_to_string('conteudos/historico_demandas.html', {'demandas_concluidas': demandas}, request=request)
        return JsonResponse({'html': html})
    else:
        return render(request, 'base.html')
    
def detalhes_demanda(request, demanda_id):
    demanda = get_object_or_404(Demanda, id=demanda_id)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "titulo": demanda.titulo_projeto,
            "status": demanda.get_status_display(),
            "urgencia": demanda.get_urgencia_display(),
            "data": demanda.data_criacao.strftime("%d/%m/%Y %H:%M"),
            "descricao": demanda.descricao,
        })
    return JsonResponse({"success": False, "message": "Requisição inválida."})
    
def deletar_demanda(request, demanda_id):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        try:
            demanda = Demanda.objects.get(id=demanda_id)
            demanda.delete()
            return JsonResponse({"success": True, "message": "Demanda deletada com sucesso."})
        except Demanda.DoesNotExist:
            return JsonResponse({"success": False, "message": "Demanda não encontrada."})
    return JsonResponse({"success": False, "message": "Requisição inválida."})    


import json

def deletar_massa_demanda(request):
    if request.method == "POST":
        try:
            # Carrega o corpo da requisição e parseia o JSON
            data = json.loads(request.body)
            ids = data.get('ids', [])
            if not ids:
                return JsonResponse({'success': False, 'message': 'Nenhuma demanda selecionada.'})

            # Excluir demandas com os IDs fornecidos
            Demanda.objects.filter(id__in=ids).delete()
            return JsonResponse({'success': True, 'message': 'Demandas excluídas com sucesso.'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Dados inválidos na requisição.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Método inválido.'})

# ======================================================
# 12. Gerador de Assinaturas
# ======================================================

def gerador_assinaturas(request):
    """
    View para gerar assinaturas via formulário.
    """
    signature = None
    if request.method == 'POST':
        form = SignatureForm(request.POST, request.FILES)
        if form.is_valid():
            signature = form.cleaned_data
            # Salvar a imagem no armazenamento de mídia
            if request.FILES.get('profile_image'):
                image = request.FILES['profile_image']
                saved_path = default_storage.save(f"uploads/{image.name}", image)
                # Adiciona o caminho completo da URL da imagem
                signature['profile_image'] = f"{settings.MEDIA_URL}{saved_path}"
    else:
        form = SignatureForm()
    
    return render(request, 'usuarios/gerador_assinaturas.html', {
        'form': form,
        'signature': signature,
    })

# ======================================================
# 13. Home
# ======================================================

def home(request):
    """
    View para a página inicial.
    """
    return render(request, 'usuarios/home.html')

# ======================================================
# 14. Recuperar Login
# ======================================================

def recuperarlogin_view(request):
    """
    View para recuperação de login.
    """
    return render(request, 'usuarios/recuperarlogin.html')

# ======================================================
# 15. Resetar Senha
# ======================================================

@csrf_protect
def password_reset_confirm_view(request, uidb64=None, token=None):
    """
    View para confirmar a redefinição de senha.
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Sua senha foi redefinida com sucesso.")
                return JsonResponse({'success': True})
            else:
                messages.error(request, "Erro ao redefinir senha.")
                return JsonResponse({'success': False, 'errors': form.errors})
        else:
            form = SetPasswordForm(user)
            return render(request, 'registration/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link inválido ou expirado.")
        return JsonResponse({'success': False, 'error': 'Link inválido ou expirado.'})

# ======================================================
# 16. Base View
# ======================================================

def base_view(request):
    """
    View para a página base.
    """
    return render(request, 'usuarios/base.html')

# ======================================================
# 17. Account Settings
# ======================================================

def account_settings_view(request):
    """
    View para configurações de conta.
    """
    return render(request, 'usuarios/account_settings.html')

# ======================================================
# 18. Assinatura Gerada
# ======================================================

def assinatura_gerada(request):
    """
    View para exibir a assinatura gerada.
    """
    return render(request, 'usuarios/assinatura_gerada.html')


# ======================================================


