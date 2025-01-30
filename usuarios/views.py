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
                return redirect('registro')  # Ou outra view válida
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
    if request.method == 'POST':
        form = EmailOrUsernameAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # Certifique-se de que o usuário foi autenticado
            if user:
                # Define o backend explicitamente
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)

                # Mostra o modal para escolha do próximo passo
                return render(request, 'usuarios/login.html', {'form': form, 'show_options': True, 'user': user})
            else:
                messages.error(request, "Erro de autenticação. Usuário inválido.")
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    else:
        form = EmailOrUsernameAuthenticationForm()

    # Verifica se o login com Google redirecionou aqui
    show_options = request.GET.get('show_options', 'false') == 'true'

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

from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.timezone import now
from datetime import timedelta
from .models import Demanda, Usuario, Membro

def dashboard(request):
    """
    View para exibir estatísticas do dashboard.
    """
    hoje = now().date()
    primeiro_dia_mes = hoje.replace(day=1)

    # 📊 Contadores principais
    total_demandas = Demanda.objects.exclude(status="concluido").exclude(visivel=False).count()
    total_usuarios = Usuario.objects.count()
    total_membros = Membro.objects.count()

    # 📌 Demandas do mês atual
    demandas_no_mes = Demanda.objects.filter(data_criacao__gte=primeiro_dia_mes).count()
    demandas_concluidas_mes = Demanda.objects.filter(status="concluido", data_criacao__gte=primeiro_dia_mes).count()
    demandas_excluidas_mes = Demanda.objects.filter(status="excluido", data_criacao__gte=primeiro_dia_mes).count()

    # 📌 Demandas por Status
    status_demandas = {
        "Novo": Demanda.objects.filter(status="novo").count(),
        "Em Andamento": Demanda.objects.filter(status="em_andamento").count(),
        "Concluído": Demanda.objects.filter(status="concluido").count(),
        "Excluído": Demanda.objects.filter(status="excluido").count(),
    }

    # 📌 Demandas Recentes (Últimas 5)
    demandas_recentes = Demanda.objects.order_by('-data_criacao')[:5]

    # 📊 Estrutura de dados para o gráfico (últimos 6 meses)
    estatisticas_mensais = []
    for i in range(6, 0, -1):
        mes_referencia = hoje - timedelta(days=i * 30)
        mes_numero = mes_referencia.month
        ano = mes_referencia.year
        nome_mes = calendar.month_abbr[mes_numero]  # Exemplo: Jan, Feb...

        total = Demanda.objects.filter(data_criacao__year=ano, data_criacao__month=mes_numero).count()
        estatisticas_mensais.append({"mes": f"{nome_mes}/{ano}", "total": total})

    # 📌 Enviar os dados para o template (AJAX ou render padrão)
    context = {
        "total_demandas": total_demandas,
        "total_usuarios": total_usuarios,
        "total_membros": total_membros,
        "demandas_no_mes": demandas_no_mes,
        "demandas_concluidas_mes": demandas_concluidas_mes,
        "demandas_excluidas_mes": demandas_excluidas_mes,
        "status_demandas": status_demandas,
        "demandas_recentes": demandas_recentes,
        "estatisticas_mensais": estatisticas_mensais,
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("conteudos/dashboard.html", context, request=request)
        return JsonResponse({"html": html, "estatisticas_mensais": estatisticas_mensais})

    return render(request, "dashboard.html", context)

    

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
        ano = 2025  # Definindo o ano para 2025
        
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
        
        # Preparar lista de meses com nome, dias e primeiro dia da semana
        meses = []
        for mes_num in range(1, 13):
            nome_mes = meses_pt_br[mes_num - 1]
            primeiro_dia_semana, dias_no_mes = calendar.monthrange(ano, mes_num)
            
            # Ajuste: Convertendo de segunda=0,..., domingo=6 para domingo=0,..., sábado=6
            primeiro_dia_semana = (primeiro_dia_semana + 1) % 7
            
            dias = []
            
            # Inserir células vazias para alinhar o primeiro dia
            for _ in range(primeiro_dia_semana):
                dias.append({'dia': None, 'demandas': []})
            
            for dia in range(1, dias_no_mes + 1):
                demandas_do_dia = demandas_por_mes_dia.get(mes_num, {}).get(dia, [])
                dias.append({
                    'dia': dia,
                    'demandas': demandas_do_dia
                })
            
            # Opcional: Inserir células vazias no final para completar a última semana
            while len(dias) % 7 != 0:
                dias.append({'dia': None, 'demandas': []})
            
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
            data_demanda_str = request.POST.get("data_demanda")  # Novo campo

            # Atualiza os campos da demanda
            demanda.titulo_projeto = titulo
            demanda.descricao = descricao
            demanda.status = status
            demanda.urgencia = urgencia
            demanda.nome_solicitante = nome_solicitante
            demanda.categoria = categoria
            demanda.taxa_urgencia = True if taxa_urgencia == "Sim" else False

            # Atualiza a data da demanda
            if data_demanda_str:
                # Converte a string para um objeto date
                data_demanda = datetime.strptime(data_demanda_str, '%Y-%m-%d').date()
                demanda.data_demanda = data_demanda

            # Atualiza o arquivo adicional se houver
            if request.FILES.get("arquivo_adicional"):
                demanda.arquivo_adicional = request.FILES.get("arquivo_adicional")

            demanda.save()

            response_data = {
                "success": True,
                "message": "Demanda atualizada com sucesso!",
                "status_display": demanda.get_status_display(),
                "data_criacao": demanda.data_criacao.strftime("%d/%m/%Y %H:%M"),
                "data_demanda": demanda.data_demanda.strftime("%d/%m/%Y"),
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
            membro.ativo = True  # Marca o membro como inativo
            membro.delete()  # Remove do banco permanentemente
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
            nome = request.POST.get('nome')
            email = request.POST.get('email')
            telefone = request.POST.get('telefone', '')
            cargo = request.POST.get('cargo', '')

            if not nome or not email:
                return JsonResponse({'error': 'Nome e email são obrigatórios!'}, status=400)

            if Membro.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email já cadastrado!'}, status=400)

            novo_membro = Membro(nome=nome, email=email, telefone=telefone, cargo=cargo)
            novo_membro.save()

            return JsonResponse({
                'message': 'Membro cadastrado com sucesso!',
                'membro': {
                    'id': novo_membro.id,
                    'nome': novo_membro.nome,
                    'email': novo_membro.email,
                    'telefone': novo_membro.telefone,
                    'cargo': novo_membro.cargo,
                }
            }, status=201)
        except Exception as e:
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


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode



def enviar_email_redefinicao(request, user):
    current_site = get_current_site(request)
    subject = 'Redefinição de Senha'
    message = render_to_string('usuarios/password_reset_email.html', {
        'user': user,
        'domain': current_site.domain,  # Domínio correto
        'protocol': 'http' if settings.DEBUG else 'https',  # HTTP para desenvolvimento, HTTPS para produção
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    user.email_user(subject, message)

