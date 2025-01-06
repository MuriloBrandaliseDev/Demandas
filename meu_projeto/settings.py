from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-2b_#&mtf9%e06i@d5^t3h11@z!i!)lsq&3jw4+@a41u$0t#-)x'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuarios',  # App de usuários
   


    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    
]

# settings.py



SITE_ID = 1



MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


ACCOUNT_EMAIL_VERIFICATION = 'none' # Desabilita a verificação de e-mail
ACCOUNT_EMAIL_VERIFICATION = 'none' # Não verificar e-mail
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none' # Não verificar o e-mail para contas sociais
SOCIALACCOUNT_QUERY_EMAIL = True # Obter o e-mail do Google
SOCIALACCOUNT_LOGIN_ON_GET = True # Login com Google'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            
            'client_id': '79146492866-bq6491u0rqfgg87tp24l09gfot0t3hjf.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        },
        'AUTH_PARAMS': {
'access_type': 'online',
# 'prompt': 'consent', # Força o Google a solicitar autorização novamente
},
'OAUTH_PKCE_ENABLED': True,
    }
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'meu_projeto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'meu_projeto.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

ACCOUNT_ADAPTER = 'usuarios.adapters.CustomAccountAdapter'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Backend padrão do Django
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_REDIRECT_URL = '/base/'  # Redireciona após login
LOGOUT_REDIRECT_URL = '/'  # Redireciona após logout

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'murilobrandalise98@gmail.com'
EMAIL_HOST_PASSWORD = 'qqzx ubwj haly khil'
DEFAULT_FROM_EMAIL = 'murilobrandalise98@gmail.com'

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




JAZZMIN_SETTINGS = {
    "site_title": "Administração",
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Administração",
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Administração",
    "changeform_format": "carousel",
    "welcome_sign": "Bem-vindo a Administração da Quero Lar",
    # Logotipo - Adicione o caminho para seu logotipo
    "site_logo": "app/img/common/logo-mini.png",
    # "search_model": ["ossystem.OS"],
    "user_avatar": 'foto',
    "changeform_format_overrides": {"auth.User": "collapsible", "auth.group": "vertical_tabs"},
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        # external url that opens in a new window (Permissions can be added)
    ],
    # User Avatar to use in the top right

    "show_ui_builder": True,
    "related_modal_active": True,
    "custom_css": None,
    "custom_js": None,
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": [],

}

# Personalization Configuration
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}