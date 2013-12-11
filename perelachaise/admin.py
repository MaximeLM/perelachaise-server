# -*- coding: utf8 -*-

from django.contrib import admin

from perelachaise.models import Tombe

class TombeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nom_court','id']}),
        ('Position', {'fields': ['latitude','longitude']}),
    ]
    list_display = ('nom_court','id')
    ordering = ('nom_court',)
    search_fields = ('nom_court',)
    readonly_fields = ('id','nom_court','latitude','longitude',)
    actions = None

# Déclaration des objets pour l'interface administrateur
admin.site.register(Tombe, TombeAdmin)
