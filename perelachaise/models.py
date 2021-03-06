#!/usr/bin/env python
# encoding: utf-8

from django.db import models

class NodeOSM(models.Model):
    """
    Représente un noeud OSM.
    """
    
    # Identifiant unique OSM <id> utilisé comme clé primaire
    # Surchargé pour ne pas générer de séquence
    id = models.BigIntegerField(primary_key=True)
    
    # Nom du node OSM <name>
    nom = models.CharField(max_length=255)
    
    # Latitude du point <lat>
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    
    # Latitude du point <lon>
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    
    # Timestamp <timestamp>
    timestamp = models.DateTimeField()
    
    # Utilisateur <user>
    utilisateur = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.nom
    
    # Méta-propriétés de la classe
    class Meta:
        # Nom verbeux au pluriel
        verbose_name_plural = u'Nodes OSM'
        
        # Règle de tri par défaut
        ordering = ('nom','id',)


class ImageCommons(models.Model):
    """
    Représente une image issue de Wikimedia Commons.
    """
    
    # Nom
    nom = models.CharField(max_length=255,unique=True)
    
    # Auteur
    auteur = models.CharField(max_length=255)
    
    # Licence
    licence = models.CharField(max_length=255)
    
    # URL de l'image originale
    url_original = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.nom
    
    # Méta-propriétés de la classe
    class Meta:
        # Nom verbeux au pluriel
        verbose_name_plural = u'Images Commons'


class Monument(models.Model):
    """
    Représente un monument, généralement une tombe, relatif à un noeud OSM.
    Il peut aussi s'agir d'un monument sans personne associée,
    comme le mur des fédérés.
    """
    
    # Noeud OSM auquel se rattache le monument
    node_osm = models.ForeignKey('NodeOSM',unique=True)
    
    # Flag indiquant si le monument a été validé pour publication
    controle = models.BooleanField(default=False)
    
    # Code wikidata, par exemple 'Q123456'
    code_wikidata = models.CharField(max_length=20, blank=True)
    
    # Code de la page wikipedia
    code_wikipedia = models.CharField(max_length=255, blank=True)
    
    # Nom complet (ex: Jim Morrison)
    nom = models.CharField(max_length=255)
    
    # Nom pour tri alphabétique (ex: Morrison)
    nom_pour_tri = models.CharField(max_length=255)
    
    # Résumé
    # Correspond en général à l'introduction de la page wikipedia
    resume = models.TextField(blank=True)
    
    # Code de la catégorie Commons
    categorie_commons = models.CharField(max_length=255, blank=True)
    
    # Image Commons principale
    image_principale = models.ForeignKey('ImageCommons',unique=True, blank=True, null=True, on_delete=models.PROTECT)
    
    # Noms verbeux
    controle.verbose_name = u'contrôle'
    resume.verbose_name = u'résumé'
    
    def save(self, *args, **kwargs):
        """ Surchargé pour supprimer les \r du champ résumé ajoutés par l'interface admin """
        self.resume = self.resume.replace('\r','')
        super(Monument, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.nom


class Personnalite(models.Model):
    """
    Représente une personnalité enterrée dans un monument.
    """
    
    # Constantes
    ANNEE = 'A'
    MOIS = 'M'
    JOUR = 'J'
    
    PRECISION_CHOICES = (
            (ANNEE, u'Année'),
            (MOIS, u'Mois'),
            (JOUR, u'Jour'),
        )
    
    # Monument où est enterrée la personnalité
    monument = models.ForeignKey('Monument')
    
    # Code wikidata, par exemple 'Q123456'
    code_wikidata = models.CharField(max_length=20, blank=True)
    
    # Code de la page wikipedia
    code_wikipedia = models.CharField(max_length=255, blank=True)
    
    # Code de la catégorie Commons
    categorie_commons = models.CharField(max_length=255, blank=True)
    
    # Nom
    nom = models.CharField(max_length=255)
    
    # Date de naissance
    date_naissance = models.DateField(blank=True, null=True)
    
    # Précision de la date de naissance
    date_naissance_precision = models.CharField(max_length=1,default=JOUR,choices=PRECISION_CHOICES)
    
    # Date de décès
    date_deces = models.DateField(blank=True, null=True)
    
    # Précision de la date de décès
    date_deces_precision = models.CharField(max_length=1,default=JOUR,choices=PRECISION_CHOICES)
    
    # Activité
    activite = models.CharField(max_length=255, blank=True)
    
    # Résumé
    # Correspond en général à l'introduction de la page wikipedia
    resume = models.TextField(blank=True)
    
    # Noms verbeux
    date_naissance.verbose_name = u'date de naissance'
    date_deces.verbose_name = u'date de décès'
    date_naissance_precision.verbose_name = u'précision date de naissance'
    date_deces_precision.verbose_name = u'précision date de décès'
    activite.verbose_name = u'activité'
    resume.verbose_name = u'résumé'
    
    def __unicode__(self):
        return self.nom
    
    def save(self, *args, **kwargs):
        """ Surchargé pour supprimer les \r du champ résumé ajoutés par l'interface admin """
        self.resume = self.resume.replace('\r','')
        super(Personnalite, self).save(*args, **kwargs)
    
    # Méta-propriétés de la classe
    class Meta:
        # Nom verbeux
        verbose_name = u'Personnalité'

class JourEvenement(models.Model):
    """
    Représente un évènement (naissance, décès, etc) ayant eu lieu un jour précis.
    """
    
    # Constantes
    NAISSANCE = u'Naissance'
    DECES = u'Décès'
    
    DESCRIPTION_CHOICES = (
            (NAISSANCE, u'Naissance'),
            (DECES, u'Décès'),
        )
    
    # Jour de l'évènement
    jour = models.DateField()
    
    # Personnalité liée à l'évènement
    personnalite = models.ForeignKey('Personnalite')
    
    # Description de l'évènement, par exemple "Naissance"
    description = models.CharField(max_length=255,default=NAISSANCE,choices=DESCRIPTION_CHOICES)
    
    # Lien wikipedia
    lien_wikipedia = models.CharField(max_length=255)
    
    # Lien wikimedia commons personnalite
    lien_commons_personnalite = models.CharField(max_length=255)
    
    # Lien wikimedia commons monument
    lien_commons_monument = models.CharField(max_length=255)
    
    def __unicode__(self):
        return (u'%s : %s %s' % (self.jour, self.description, self.personnalite.nom))
    
    class Meta:
        unique_together = ('personnalite', 'description',)
