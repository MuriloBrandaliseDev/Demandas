from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Profile, Demanda

@admin.register(Demanda)
class DemandaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "descricao", "status", "urgencia", "data_criacao")


# admin.py



class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil'

class UsuarioAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'telefone', 'endereco', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('telefone', 'endereco')}),
    )

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Demanda)
