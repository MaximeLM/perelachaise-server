# -*- coding: utf8 -*-

from django.contrib import admin
from django.db import models

from perelachaise.models import NodeOSM, Monument, Personnalite, ImageCommons

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
                    'nombre_monuments',
                    'utilisateur','timestamp')
    
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
        (u'Modification', {'fields': ['utilisateur','timestamp']}),
    ]
    
    # ====================
    # Méthodes d'affichage
    # ====================
    
    def nombre_monuments(self, obj):
        """ Affiche le nombre de monuments liés au node OSM """
        return obj.monument_set.count()
    
    # Nom verbeux
    nombre_monuments.short_description = u'nombre de monuments'
    
    # Règle de tri
    nombre_monuments.admin_order_field = 'monument__count'
    
    def queryset(self, request):
        """ Surcharge permettant le tri de la liste
        par des règles calculées """
        qs = super(NodeOSMAdmin, self).queryset(request)
        qs = qs.annotate(models.Count('monument'))
        return qs


class ImageCommonsAdmin(admin.ModelAdmin):
    """
    Classe d'administration de ImageCommons
    """
    
    # ================
    # Liste des objets
    # ================
    
    # Liste des champs affichés
    list_display = ('nom','lien_commons','auteur','licence','id',
                    'nombre_monuments',)
    
    # Règle de tri par défaut
    ordering = ('nom','id',)
    
    # Liste des champs recherchables
    search_fields = ('nom',)
    
    # Actions administrateur disponibles
    actions=None
    
    # Champs en lecture seule
    readonly_fields = ('id','lien_commons','original',)
    
    # =================
    # Détail d'un objet
    # =================
    
    # Liste des champs affichés
    fieldsets = [
        (None, {'fields': ['id','nom','lien_commons','auteur','licence','url_original','original']}),
    ]
    
    # ====================
    # Méthodes d'affichage
    # ====================
    
    def lien_commons(self,obj):
        """ Affiche le lien vers l'image dans Wikimedia Commons """
        url_commons = 'http://commons.wikimedia.org/wiki/File:' + obj.nom.encode('utf8')
        return '<a href="%s">%s</a>' % (url_commons, obj.nom.encode('utf8'))
    
    lien_commons.allow_tags = True
    
    def original(self,obj):
        """ Affiche l'url de l'image originale """
        if obj.url_original:
            return u'<a href="%s">%s</a>' % (obj.url_original,obj.url_original)
        else:
            return u''
    
    original.allow_tags = True
    
    # Règle de tri
    lien_commons.admin_order_field = 'nom'
    
    def nombre_monuments(self, obj):
        """ Affiche le nombre de monuments liés à l'image """
        return obj.monument_set.count()
    
    # Nom verbeux
    nombre_monuments.short_description = u'nombre de monuments'
    
    # Règle de tri
    nombre_monuments.admin_order_field = 'monument__count'
    
    def queryset(self, request):
        """ Surcharge permettant le tri de la liste
        par des règles calculées """
        qs = super(ImageCommonsAdmin, self).queryset(request)
        qs = qs.annotate(models.Count('monument'))
        return qs


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
        (None, {'fields': ['nom','id',
                           'code_wikidata',
                           'lien_wikidata',
                           'code_wikipedia',
                           'lien_wikipedia',
                           'categorie_commons',
                           'lien_commons',
                           'date_naissance',
                           'date_naissance_precision',
                           'date_deces',
                           'date_deces_precision',
                           'activite',
                           'resume',
                           'resume_formatted',
                                ]}),
    ]
    
    # Champs en lecture seule
    readonly_fields = ('id','lien_wikidata','lien_wikipedia','lien_commons','resume_formatted',)
    
    # ====================
    # Méthodes d'affichage
    # ====================
    
    def lien_wikidata(self, obj):
        """ Affiche un lien vers la page wikidata """
        if obj.code_wikidata:
            return '<a href="http://www.wikidata.org/wiki/%s?uselang=fr">%s</a>' % (obj.code_wikidata, obj.code_wikidata)
        else:
            return None
    
    lien_wikidata.allow_tags = True
    
    def lien_wikipedia(self, obj):
        """ Affiche un lien vers la page wikipedia """
        if obj.code_wikipedia:
            url_wikipedia = 'http://fr.wikipedia.org/wiki/' + obj.code_wikipedia.encode('utf8')
            return '<a href="%s">%s</a>' % (url_wikipedia, obj.code_wikipedia.encode('utf8'))
        else:
            return ''
    
    lien_wikipedia.allow_tags = True
    
    def lien_commons(self, obj):
        """ Affiche un lien vers la page wikimedia commons """
        if obj.categorie_commons:
            url_commons = 'http://commons.wikimedia.org/wiki/Category:' + obj.categorie_commons.encode('utf8')
            return '<a href="%s">%s</a>' % (url_commons, obj.categorie_commons.encode('utf8'))
        else:
            return ''
    
    lien_commons.allow_tags = True
    
    def nom_complet(self, obj):
        """ Affiche le nom complet de l'objet """
        return unicode(obj)
    
    def resume_formatted(self, obj):
        """ Affiche le résumé au format HTML en complétant les liens internes wikipedia """
        resume = obj.resume.replace('<a href="/wiki/','<a href="http://fr.wikipedia.org/wiki/').replace('\n','')
        return resume
    
    # Autorisation du lien HTTP
    resume_formatted.allow_tags = True
    
    # Nom verbeux
    resume_formatted.short_description = u'Résumé (HTML)'


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
                    'lien_image_principale_liste',
                    'activite',
                    'wikidata','wikipedia','commons',
                    'nombre_personnalites')
    
    # Règle de tri par défaut
    ordering = ('controle','nom_pour_tri','nom',)
    
    # Liste des champs recherchables
    search_fields = ('nom',)
    
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
        (u'Image principale', {'fields': ['image_principale',
                                          'lien_image_principale_detail',
                                          'lien_commons',
                                          'auteur',
                                          'licence',
                                          'original'
                                          ]}),
        (u'Monument', {'fields': ['id','nom','nom_pour_tri',
                                'code_wikidata',
                                'lien_wikidata',
                                'code_wikipedia',
                                'lien_wikipedia',
                                'categorie_commons',
                                'lien_categorie_commons',
                                'resume',
                                'resume_formatted'
                                ]}),
    ]
    
    # Champs en lecture seule
    readonly_fields = ('id','lien_wikidata','lien_wikipedia','lien_categorie_commons','resume_formatted','auteur','licence',
                        'id_osm','latitude','longitude','lien_node_osm_detail','lien_image_principale_detail','lien_commons',
                        'original')
    
    # Affichage des personnalités liées
    inlines = [
        PersonnaliteInline,
    ]
    
    # ====================
    # Méthodes d'affichage
    # ====================
    
    def lien_wikidata(self, obj):
        """ Affiche un lien vers la page wikidata du monument """
        if obj.code_wikidata:
            return '<a href="http://www.wikidata.org/wiki/%s?uselang=fr">%s</a>' % (obj.code_wikidata, obj.code_wikidata)
        else:
            return ''
    
    # Autorisation du lien HTTP
    lien_wikidata.allow_tags = True
    
    def lien_wikipedia(self, obj):
        """ Affiche un lien vers la page wikipedia du monument """
        if obj.code_wikipedia:
            url_wikipedia = 'http://fr.wikipedia.org/wiki/' + obj.code_wikipedia
            return '<a href="%s">%s</a>' % (url_wikipedia, obj.code_wikipedia)
        else:
            return ''
    
    # Autorisation du lien HTTP
    lien_wikipedia.allow_tags = True
    
    def lien_categorie_commons(self, obj):
        """ Affiche un lien vers la page wikimedia commons du monument """
        if obj.categorie_commons:
            url_commons = 'http://commons.wikimedia.org/wiki/Category:' + obj.categorie_commons
            return '<a href="%s">%s</a>' % (url_commons, obj.categorie_commons)
        else:
            return ''
    
    # Autorisation du lien HTTP
    lien_categorie_commons.allow_tags = True
    
    def wikidata(self, obj):
        """ Affiche un lien vers la page wikidata calculée """
        if obj.personnalite_set.count() == 1:
            # Si exactement 1 personnalité est liée à ce monument :
            # affichage du lien de la personnalité
            personnalite = Personnalite.objects.get(monument=obj.id)
            if personnalite.code_wikidata:
                return '<a href="http://www.wikidata.org/wiki/%s?uselang=fr">%s</a>' % (personnalite.code_wikidata, personnalite.code_wikidata)
            else:
                return ''
        else:
            # Affichage du lien du monument
            if obj.code_wikidata:
                return '<a href="http://www.wikidata.org/wiki/%s?uselang=fr">%s</a>' % (obj.code_wikidata, obj.code_wikidata)
            else:
                return ''
    
    # Autorisation du lien HTTP
    wikidata.allow_tags = True
    
    # Nom verbeux
    wikidata.short_description = u'lien Wikidata'
    
    def wikipedia(self, obj):
        """ Affiche un lien vers la page wikipedia calculée """
        if obj.personnalite_set.count() == 1:
            # Si exactement 1 personnalité est liée à ce monument :
            # affichage du lien de la personnalité
            personnalite = Personnalite.objects.get(monument=obj.id)
            if personnalite.code_wikipedia:
                url_wikipedia = 'http://fr.wikipedia.org/wiki/' + personnalite.code_wikipedia.encode('utf8')
                return '<a href="%s">%s</a>' % (url_wikipedia, personnalite.code_wikipedia.encode('utf8'))
            else:
                return ''
        else:
            # Affichage du lien du monument
            if obj.code_wikipedia:
                url_wikipedia = 'http://fr.wikipedia.org/wiki/' + obj.code_wikipedia.encode('utf8')
                return '<a href="%s">%s</a>' % (url_wikipedia, obj.code_wikipedia.encode('utf8'))
            else:
                return ''
    
    # Autorisation du lien HTTP
    wikipedia.allow_tags = True
    
    # Nom verbeux
    wikipedia.short_description = u'lien Wikipedia'
    
    def commons(self, obj):
        """ Affiche un lien vers la page wikimedia commons du monument """
        # Affichage du lien du monument
        if obj.categorie_commons:
            url_commons = 'http://commons.wikimedia.org/wiki/Category:' + obj.categorie_commons.encode('utf8')
            return '<a href="%s">%s</a>' % (url_commons, obj.categorie_commons.encode('utf8'))
        else:
            return ''
    
    # Autorisation du lien HTTP
    commons.allow_tags = True
    
    # Nom verbeux
    commons.short_description = u'lien Wikimedia Commons'
    
    def activite(self, obj):
        """ Affiche l'activité de la personnalité associée si elle est unique"""
        if obj.personnalite_set.count() == 1:
            # Si exactement 1 personnalité est liée à ce monument :
            personnalite = Personnalite.objects.get(monument=obj.id)
            return personnalite.activite
        else:
            return ''
    
    # Nom verbeux
    activite.short_description = u'activité'
    
    def lien_node_osm_liste(self, obj):
        """ Affiche un lien vers la page d'administration
        du node OSM associé à partir de la liste d'objets.
        Différencié pour le chemin relatif. """
        return '<a href="../nodeosm/%d">%s</a>' % (obj.node_osm.id,obj.node_osm.nom)
    
    # Autorisation du lien HTTP
    lien_node_osm_liste.allow_tags = True
    
    # Nom verbeux
    lien_node_osm_liste.short_description = u'node OSM'
    
    # Règle de tri
    lien_node_osm_liste.admin_order_field = 'node_osm__nom'
    
    def lien_node_osm_detail(self, obj):
        """ Affiche un lien vers la page d'administration
        du node OSM associé à partir de la vue détaillée.
        Différencié pour le chemin relatif. """
        return '<a href="../../nodeosm/%d">%s</a>' % (obj.node_osm.id,obj.node_osm.nom)
    
    # Autorisation du lien HTTP
    lien_node_osm_detail.allow_tags = True
    
    # Nom verbeux
    lien_node_osm_detail.short_description = u'node OSM'
    
    def lien_image_principale_liste(self, obj):
        """ Affiche un lien vers la page d'administration
        de l'image commons associé à partir de la liste d'objets.
        Différencié pour le chemin relatif. """
        
        if obj.image_principale:
            return '<a href="../imagecommons/%d">%s</a>' % (obj.image_principale.id,obj.image_principale.nom)
        else:
            return u''
    
    # Autorisation du lien HTTP
    lien_image_principale_liste.allow_tags = True
    
    # Nom verbeux
    lien_image_principale_liste.short_description = u'image principale'
    
    # Règle de tri
    lien_image_principale_liste.admin_order_field = 'image_principale__nom'
    
    def lien_image_principale_detail(self, obj):
        """ Affiche un lien vers la page d'administration
        de l'image commons associé à partir de la vue détaillée.
        Différencié pour le chemin relatif. """
        
        if obj.image_principale:
            return '<a href="../../imagecommons/%d">%s</a>' % (obj.image_principale.id,obj.image_principale.nom)
        else:
            return None
    
    # Autorisation du lien HTTP
    lien_image_principale_detail.allow_tags = True
    
    # Nom verbeux
    lien_image_principale_detail.short_description = u'image principale'
    
    def nom_complet(self, obj):
        """ Affiche le nom complet de l'objet """
        return unicode(obj)
    
    # Nom verbeux
    nom_complet.short_description = u'nom'
    
    # Règle de tri
    nom_complet.admin_order_field = 'nom_pour_tri'
    
    def nombre_personnalites(self, obj):
        """ Affiche le nombre de personnalités liées au monument"""
        return obj.personnalite_set.count()
    
    # Nom verbeux
    nombre_personnalites.short_description = u'nombre de personnalités'
    
    # Règle de tri
    nombre_personnalites.admin_order_field = 'personnalite__count'
    
    def id_osm(self, obj):
        """ Affiche l'id du node OSM lié """
        if obj.node_osm:
            return obj.node_osm.id
        else:
            return None
    
    def latitude(self, obj):
        """ Affiche la latitude du node OSM lié """
        if obj.node_osm:
            return obj.node_osm.latitude
        else:
            return None
    
    def longitude(self, obj):
        """ Affiche la longitude du node OSM lié """
        if obj.node_osm:
            return obj.node_osm.longitude
        else:
            return None
    
    def resume_formatted(self, obj):
        """ Affiche le résumé au format HTML en complétant les liens internes wikipedia """
        resume = obj.resume.replace('<a href="/wiki/','<a href="http://fr.wikipedia.org/wiki/').replace('\n','')
        return resume
    
    # Autorisation du lien HTTP
    resume_formatted.allow_tags = True
    
    # Nom verbeux
    resume_formatted.short_description = u'Résumé (HTML)'
    
    def auteur(self, obj):
        """ Affiche l'auteur de l'image principale """
        if obj.image_principale:
            return obj.image_principale.auteur
        else:
            return u''
    
    def licence(self,obj):
        """ Affiche la licence de l'image principale """
        if obj.image_principale:
            return obj.image_principale.licence
        else:
            return u''
    
    def lien_commons(self,obj):
        """ Affiche le lien vers l'image dans Wikimedia Commons """
        if obj.image_principale:
            url_commons = 'http://commons.wikimedia.org/wiki/File:' + obj.image_principale.nom.encode('utf8')
            return '<a href="%s">%s</a>' % (url_commons, url_commons)
        else:
            return u''
    
    lien_commons.allow_tags = True
    
    def original(self,obj):
        """ Affiche l'url de l'image originale """
        if obj.image_principale and obj.image_principale.url_original:
            return u'<a href="%s">%s</a>' % (obj.image_principale.url_original,obj.image_principale.url_original)
        else:
            return u''
    
    original.allow_tags = True
    
    def queryset(self, request):
        """ Surcharge permettant le tri de la liste
        par des règles calculées """
        qs = super(MonumentAdmin, self).queryset(request)
        qs = qs.annotate(models.Count('personnalite'))
        return qs


# Déclaration des classes pour l'interface administrateur
admin.site.register(NodeOSM, NodeOSMAdmin)
admin.site.register(ImageCommons, ImageCommonsAdmin)
admin.site.register(Monument, MonumentAdmin)
