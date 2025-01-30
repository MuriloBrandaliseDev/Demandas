from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from .views import deletar_demanda
from .views import gerar_relatorio_excel
from .views import excluir_membro

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('recuperarlogin/', views.recuperarlogin_view, name='recuperarlogin'),
    path('base/', views.base_view, name='base'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
    path('equipe/', views.equipe, name='equipe'),
    path('calendario/', views.calendario, name='calendario'),
    path('gerador-assinaturas/', views.gerador_assinaturas, name='gerador_assinaturas'),
    path('excluir-demanda/<int:demanda_id>/', views.excluir_demanda, name='excluir_demanda'),
    path('concluir-demanda/<int:demanda_id>/', views.concluir_demanda, name='concluir_demanda'),
    path('historico/', views.historico_demandas, name='historico_demandas'),
    path("detalhes-demanda/<int:demanda_id>/", views.detalhes_demanda, name="detalhes_demanda"),
    path('editar-demanda/<int:demanda_id>/', views.editar_demanda, name='editar_demanda'),
    path("deletar-demanda/<int:demanda_id>/", deletar_demanda, name="deletar_demanda"),
    path('deletar-massa-demanda/', views.deletar_massa_demanda, name='deletar_massa_demanda'),
    path('cadastrar-membro/', views.cadastrar_membro, name='cadastrar_membro'),
    path('excluir-membro/<int:membro_id>/', excluir_membro, name='excluir_membro'),
    path('editar-membro/<int:membro_id>/', views.editar_membro, name='editar_membro'),
    path("gerar-relatorio/", gerar_relatorio_excel, name="gerar_relatorio"),
    
    
    
    
    
    # URLs para a recuperação de senha usando auth_views do Django
    path('recuperar-senha/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('recuperar-senha-enviada/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('resetar-senha/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('senha-resetada/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
