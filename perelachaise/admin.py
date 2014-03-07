# -*- coding: utf8 -*-

from django.contrib import admin
from django.db import models

from perelachaise.models import NodeOSM, Monument, Personnalite

class NodeOSMAdmin(admin.ModelAdmin):
    """
    Classe d'administration de NodeOSM
    """
    
    # ================
    # Liste des objets
    # ================
    
    # Liste des champs affichés
    list_display = ('nom','id',
                    'latitude','longitude')
    
    # Règle de tri par défaut
    ordering = ('nom','id',)
    
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
    ]


class PersonnaliteInline(admin.StackedInline):
    """
    Classe d'administration inline de Personnalite
    """
    
    # Classe modèle
    model = Personnalite
    
    # Nombre de formulaires vides
    extra = 0
    
    # =================
    # Détail d'un objet
    # =================
    
    # Liste des champs affichés
    fieldsets = [
        (None, {'fields': ['nom',
                           'code_wikidata',
                           'lien_wikidata',
                           'url_wikipedia',
                           'date_naissance',
                           'date_deces',
                           'activite',
                           'resume',
                                ]}),
    ]
    
    # Champs en lecture seule
    readonly_fields = ('lien_tombe','lien_wikidata',)
    
    # ====================
    # Méthodes d'affichage
    # ====================
    
    def lien_wikidata(self, obj):
        ''' Affiche un lien vers la page wikidata '''
        if obj.code_wikidata:
            return '<a href="http://www.wikidata.org/wiki/%s?uselang=fr">http://www.wikidata.org/wiki/%s?uselang=fr</a>' % (obj.code_wikidata, obj.code_wikidata)
        else:
            return None
    
    lien_wikidata.allow_tags = True
    
    def lien_wikipedia(self, obj):
        ''' Affiche un lien vers la page wikipedia '''
        return '<a href="%s">%s</a>' % (obj.url_wikipedia, obj.url_wikipedia)
    
    lien_wikipedia.allow_tags = True
    
    def lien_tombe(self, obj):
        ''' Affiche un lien vers la page d'administration
        de la tombe associée '''
        return '<a href="../../monument/%d">%s</a>' % (obj.tombe.id,unicode(obj.tombe))
    
    lien_tombe.allow_tags = True
    
    def nom_complet(self, obj):
        ''' Affiche le nom complet de l'objet '''
        return unicode(obj)


class MonumentAdmin(admin.ModelAdmin):
    """
    Classe d'administration de Monument
    """
    
    # ================
    # Liste des objets
    # ================
    
    # Liste des champs affichés
    list_display = ('nom_complet','controle',
                    'lien_node_osm_liste',
                    'wikidata','wikipedia',
                    'nombre_personnalites')
    
    # Règle de tri par défaut
    ordering = ('nom',)
    
    # Liste des champs recherchables
    search_fields = ('nom','prenom')
    
    # Actions administrateur disponibles
    actions=None
    
    # =================
    # Détail d'un objet
    # =================
    
    # Liste des champs affichés
    fieldsets = [
        (None, {u'fields': ['controle']}),
        (u'Node OSM', {'fields': ['node_osm',
                                  'lien_node_osm_detail',
                                  'id_osm',
                                  'latitude',
                                  'longitude'
                                  ]}),
        (u'Monument', {'fields': ['prenom','nom',
                                'code_wikidata',
                                'lien_wikidata',
                                'url_wikipedia',
                                'resume',
                                ]}),
    ]
    
    # Champs en lecture seule
    readonly_fields = ('lien_wikidata',
                        'id_osm','latitude','longitude','lien_node_osm_detail')
    
    # Affichage des personnalités liées
    inlines = [
        PersonnaliteInline,
    ]
    
    # ====================
    # Méthodes d'affichage
    # ====================
    
    def lien_wikidata(self, obj):
        ''' Affiche un lien vers la page wikidata du monument '''
        if obj.code_wikidata:
            return '<a href="http://www.wikidata.org/wiki/%s?uselang=fr">http://www.wikidata.org/wiki/%s?uselang=fr</a>' % (obj.code_wikidata, obj.code_wikidata)
        else:
            return ''
    
    # Autorisation du lien HTTP
    lien_wikidata.allow_tags = True
    
    def lien_wikipedia(self, obj):
        ''' Affiche un lien vers la page wikipedia du monument '''
        return '<a href="%s">%s</a>' % (obj.url_wikipedia, obj.url_wikipedia)
    
    # Autorisation du lien HTTP
    lien_wikipedia.allow_tags = True
    
    def wikidata(self, obj):
        ''' Affiche un lien vers la page wikidata calculée '''
        if obj.personnalite_set.count() == 1:
            # Si exactement 1 personnalité est liée à ce monument :
            # affichage du lien de la personnalité
            personnalite = Personnalite.objects.get(tombe=obj.id)
            if personnalite.code_wikidata:
                return '<a href="http://www.wikidata.org/wiki/%s?uselang=fr">http://www.wikidata.org/wiki/%s?uselang=fr</a>' % (personnalite.code_wikidata, personnalite.code_wikidata)
            else:
                return None
        else:
            # Affichage du lien du monument
            if obj.code_wikidata:
                return '<a href="http://www.wikidata.org/wiki/%s?uselang=fr">http://www.wikidata.org/wiki/%s?uselang=fr</a>' % (obj.code_wikidata, obj.code_wikidata)
            else:
                return ''
    
    # Autorisation du lien HTTP
    wikidata.allow_tags = True
    
    # Nom verbeux
    wikidata.short_description = u'lien Wikidata'
    
    # Règle de tri
    wikidata.admin_order_field = 'code_wikidata'
    
    def wikipedia(self, obj):
        ''' Affiche un lien vers la page wikipedia calculée '''
        if obj.personnalite_set.count() == 1:
            # Si exactement 1 personnalité est liée à ce monument :
            # affichage du lien de la personnalité
            personnalite = Personnalite.objects.get(tombe=obj.id)
            return '<a href="%s">%s</a>' % (personnalite.url_wikipedia, personnalite.url_wikipedia)
        else:
            # Affichage du lien du monument
            return '<a href="%s">%s</a>' % (obj.url_wikipedia, obj.url_wikipedia)
    
    # Autorisation du lien HTTP
    wikipedia.allow_tags = True
    
    # Nom verbeux
    wikipedia.short_description = u'lien Wikipedia'
    
    # Règle de tri
    wikipedia.admin_order_field = 'url_wikipedia'
    
    def lien_node_osm_liste(self, obj):
        ''' Affiche un lien vers la page d'administration
        du node OSM associé à partir de la liste d'objets.
        Différencié pour le chemin relatif. '''
        return '<a href="../nodeosm/%d">%s</a>' % (obj.node_osm.id,obj.node_osm.nom)
    
    # Autorisation du lien HTTP
    lien_node_osm_liste.allow_tags = True
    
    # Nom verbeux
    lien_node_osm_liste.short_description = u'node OSM'
    
    # Règle de tri
    lien_node_osm_liste.admin_order_field = 'node_osm__nom'
    
    def lien_node_osm_detail(self, obj):
        ''' Affiche un lien vers la page d'administration
        du node OSM associé à partir de la vue détaillée.
        Différencié pour le chemin relatif. '''
        return '<a href="../../nodeosm/%d">%s</a>' % (obj.node_osm.id,obj.node_osm.nom)
    
    # Autorisation du lien HTTP
    lien_node_osm_detail.allow_tags = True
    
    # Nom verbeux
    lien_node_osm_detail.short_description = u'node OSM'
    
    def nom_complet(self, obj):
        ''' Affiche le nom complet de l'objet '''
        return unicode(obj)
    
    # Règle de tri
    nom_complet.admin_order_field = 'nom'
    
    def nombre_personnalites(self, obj):
        ''' Affiche le nombre de personnalités liées au monument'''
        return obj.personnalite_set.count()
    
    # Nom verbeux
    nombre_personnalites.short_description = u'nombre de personnalités'
    
    # Règle de tri
    nombre_personnalites.admin_order_field = '-personnalite__count'
    
    def id_osm(self, obj):
        ''' Affiche l'id du node OSM lié '''
        if obj.node_osm:
            return obj.node_osm.id
        else:
            return None
    
    def latitude(self, obj):
        ''' Affiche la latitude du node OSM lié '''
        if obj.node_osm:
            return obj.node_osm.latitude
        else:
            return None
    
    def longitude(self, obj):
        ''' Affiche la longitude du node OSM lié '''
        if obj.node_osm:
            return obj.node_osm.longitude
        else:
            return None
    
    def queryset(self, request):
        """ Surcharge permettant le tri de la liste
        par des règles calculées """
        qs = super(MonumentAdmin, self).queryset(request)
        qs = qs.annotate(models.Count('personnalite'))
        return qs


# Déclaration des classes pour l'interface administrateur
admin.site.register(NodeOSM, NodeOSMAdmin)
admin.site.register(Monument, MonumentAdmin)
