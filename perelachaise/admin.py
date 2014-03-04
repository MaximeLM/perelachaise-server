# -*- coding: utf8 -*-

from django.contrib import admin

from perelachaise.models import Tombe, NodeOSM, DetailTombe

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

class NodeOSMAdmin(admin.ModelAdmin):
    """
    Classe d'administration de NodeOSM
    """
    
    # ================
    # Liste des objets
    # ================
    
    # Liste des champs affichés
    list_display = ('nom','id',
                    'latitude','longitude',
                    'date_creation','date_modification')
    
    # Ordre par défaut des champs
    ordering = ('nom',)
    
    # Liste des champs recherchables
    search_fields = ('nom',)
    
    # Actions administrateur disponibles
    actions=None
    
    # =================
    # Détail d'un objet
    # =================
    
    # Liste des champs affichés
    fieldsets = [
        (None, {'fields': ['id','nom']}),
        (u'Position', {'fields': ['latitude','longitude']}),
        (u'Suivi', {'fields': ['date_creation','date_modification']}),
    ]
    
    # Champs en lecture seule
    readonly_fields = ('date_creation','date_modification',)

class DetailTombeAdmin(admin.ModelAdmin):
    """
    Classe d'administration de DetailTombe
    """
    
    # ================
    # Liste des objets
    # ================
    
    # Liste des champs affichés
    list_display = ('nom_complet','controle',
                    'lien_wikidata','lien_wikipedia',
                    'date_creation','date_modification')
    
    # Ordre par défaut des champs
    ordering = ('nom',)
    
    # Liste des champs recherchables
    search_fields = ('nom',)
    
    # Actions administrateur disponibles
    actions=None
    
    # =================
    # Détail d'un objet
    # =================
    
    # Liste des champs affichés
    fieldsets = [
        (None, {u'fields': ['node_osm','lien_node_osm']}),
        (u'Détail', {'fields': ['prenom',
                                'nom',
                                'code_wikidata',
                                'lien_wikidata',
                                'url_wikipedia',
                                'date_naissance',
                                'date_deces',
                                'activite',
                                'resume',
                                ]}),
        (u'Suivi', {'fields': ['date_creation','date_modification']}),
        (None, {u'fields': ['controle']}),
    ]
    
    # Champs en lecture seule
    readonly_fields = ('date_creation','date_modification',
                       'lien_node_osm','lien_wikidata',)
    
    # ====================
    # Méthodes d'affichage
    # ====================
    
    def lien_wikidata(self, obj):
        ''' Affiche un lien vers la page wikidata '''
        return '<a href="http://www.wikidata.org/wiki/%s?uselang=fr">%s</a>' % (obj.code_wikidata, obj.code_wikidata)
    lien_wikidata.allow_tags = True
    
    def lien_wikipedia(self, obj):
        ''' Affiche un lien vers la page wikipedia '''
        return '<a href="%s">%s</a>' % (obj.url_wikipedia, obj.url_wikipedia)
    lien_wikipedia.allow_tags = True
    
    def lien_node_osm(self, obj):
        ''' Affiche un lien vers la page d'administration
        du node OSM associé '''
        return '<a href="../../nodeosm/%d">%s</a>' % (obj.node_osm.id,obj.node_osm.nom)
    lien_node_osm.allow_tags = True
    
    def nom_complet(self, obj):
        ''' Affiche le nom complet de l'objet '''
        return unicode(obj)

# Déclaration des classes pour l'interface administrateur
admin.site.register(Tombe, TombeAdmin)
admin.site.register(NodeOSM, NodeOSMAdmin)
admin.site.register(DetailTombe, DetailTombeAdmin)
