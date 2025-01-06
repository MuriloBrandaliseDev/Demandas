from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),  # Incluímos as URLs do app `usuarios`
    path('accounts/', include('allauth.urls')),  # Inclua o allauth aqui
    
    # Rotas de autenticação 
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('alterar-senha/', auth_views.PasswordChangeView.as_view(), name='alterar_senha'),
    path('alterar-senha/done/', auth_views.PasswordChangeDoneView.as_view(), name='alterar_senha_feito'),
    path('recuperar-senha/', auth_views.PasswordResetView.as_view(), name='recuperar_senha'),
    path('recuperar-senha/done/', auth_views.PasswordResetDoneView.as_view(), name='recuperar_senha_feito'),
    path('resetar-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='resetar_senha'),
    path('resetar-senha/done/', auth_views.PasswordResetCompleteView.as_view(), name='resetar_senha_feito'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



