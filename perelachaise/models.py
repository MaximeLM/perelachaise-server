#!/usr/bin/env python
# encoding: utf-8

from django.db import models

class Tombe(models.Model):
    """
    Définit une tombe
    """
    nom_osm = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    prenom = models.CharField(max_length=255, blank=True)
    nom = models.CharField(max_length=255)
    date_naissance = models.DateField(blank=True, null=True)
    date_deces = models.DateField(blank=True, null=True)
    activite = models.CharField(max_length=255, blank=True)
    resume = models.TextField(blank=True)
    url_wikipedia = models.URLField(blank=True)
    
    def __unicode__(self):
        return self.nom_osm

class NodeOSM(models.Model):
    """
    Représente un noeud OSM correspondant à une tombe.
    """
    
    # Identifiant unique OSM <id> utilisé comme clé primaire
    # Surchargé pour ne pas générer de séquence
    id = models.IntegerField(primary_key=True)
    
    # Nom du node OSM <name>
    nom = models.CharField(max_length=255)
    
    # Latitude du point <lat>
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    
    # Latitude du point <lon>
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    
    # ==========
    # Timestamps
    # ==========
    
    # Date de création
    # Mis à jour à la création de l'objet
    date_creation = models.DateTimeField(auto_now_add=True)
    
    # Date de modification
    # Mis à jour à la sauvegarde de l'objet
    date_modification = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.nom

class DetailTombe(models.Model):
    """
    Définit une personne ou un monument relatif à un noeud OSM.
    """
    
    # Noeud OSM auquel se rattache le détail
    node_osm = models.ForeignKey('NodeOSM')
    
    # Flag indiquant si l'objet a été validé pour publication
    controle = models.BooleanField(default=False)
    
    # =================
    # Champs optionnels
    # =================
    
    # Code wikidata, par exemple 'Q123456'
    code_wikidata = models.CharField(max_length=20, blank=True)
    
    # URL de la page wikipedia
    url_wikipedia = models.URLField(blank=True)
    
    # Prénom
    prenom = models.CharField(max_length=255, blank=True)
    
    # Nom
    nom = models.CharField(max_length=255)
    
    # Date de naissance
    date_naissance = models.DateField(blank=True, null=True)
    
    # Date de décès
    date_deces = models.DateField(blank=True, null=True)
    
    # Activité
    activite = models.CharField(max_length=255, blank=True)
    
    # Résumé
    # Correspond en général à l'introduction de la page wikipedia
    resume = models.TextField(blank=True)
    
    # ==========
    # Timestamps
    # ==========
    
    # Date de création
    # Mis à jour à la création de l'objet
    date_creation = models.DateTimeField(auto_now_add=True)
    
    # Date de modification
    # Mis à jour à la sauvegarde de l'objet
    date_modification = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        if not self.prenom:
            # Pas de prénom : affichage du nom seul
            return self.nom
        else:
            # Prénom présent : affichage concaténé
            return self.prenom + ' ' + self.nom
