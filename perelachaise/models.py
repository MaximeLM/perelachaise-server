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
