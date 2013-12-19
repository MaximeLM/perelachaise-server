# -*- coding: utf8 -*-

from django.contrib import admin

from perelachaise.models import Tombe

class TombeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['id','nom_osm']}),
        ('Position', {'fields': ['latitude','longitude']}),
        (u'Détail', {'fields': ['prenom',
                                'nom',
                                'date_naissance',
                                'date_deces',
                                'activite',
                                'resume',
                                'url_wikipedia'
                                ]}),
    ]
    list_display = ('nom_osm','activite','lien_wikipedia','id')
    ordering = ('nom',)
    search_fields = ('nom_osm',)
    readonly_fields = ('id',)
    actions = None
    
    def lien_wikipedia(self, obj):
        return '<a href="%s">%s</a>' % (obj.url_wikipedia, obj.url_wikipedia)
    lien_wikipedia.allow_tags = True

# Déclaration des objets pour l'interface administrateur
admin.site.register(Tombe, TombeAdmin)
