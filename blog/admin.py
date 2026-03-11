from django.contrib import admin
from django import forms
from .models import Categoria, Post

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'titulo':
            kwargs['widget'] = forms.TextInput(attrs={'size': 80})
        elif db_field.name == 'contenido':
            kwargs['widget'] = forms.Textarea(attrs={'rows': 15, 'cols': 80})
        return super().formfield_for_dbfield(db_field, **kwargs)

class CategoriaAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Post, PostAdmin)