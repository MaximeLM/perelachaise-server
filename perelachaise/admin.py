# -*- coding: utf8 -*-

from django.contrib import admin

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
    list_display = ('nom_monument','controle',
                    'wikidata','wikipedia',
                    'nombre_personnalites')
    
    # Ordre par défaut des champs
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
    readonly_fields = ('lien_node_osm','lien_wikidata',
                        'id_osm','latitude','longitude')
    
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
    lien_wikidata.allow_tags = True
    
    
    def lien_wikipedia(self, obj):
        ''' Affiche un lien vers la page wikipedia du monument '''
        return '<a href="%s">%s</a>' % (obj.url_wikipedia, obj.url_wikipedia)
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
    wikidata.allow_tags = True
    
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
    wikipedia.allow_tags = True
    
    def lien_node_osm(self, obj):
        ''' Affiche un lien vers la page d'administration
        du node OSM associé '''
        return '<a href="../../nodeosm/%d">%s</a>' % (obj.node_osm.id,obj.node_osm.nom)
    lien_node_osm.allow_tags = True
    
    def nom_monument(self, obj):
        ''' Affiche le nom complet de l'objet '''
        return unicode(obj)
    nom_monument.admin_order_field = 'nom'
    
    def nombre_personnalites(self, obj):
        ''' Affiche le nombre de personnalités liées au monument'''
        return obj.personnalite_set.count()
    
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


# Déclaration des classes pour l'interface administrateur
admin.site.register(NodeOSM, NodeOSMAdmin)
admin.site.register(Monument, MonumentAdmin)
