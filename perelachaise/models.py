#!/usr/bin/env python
# encoding: utf-8

from django.db import models

class Tombe(models.Model):
    """
    Définit une tombe
    """
    nom_court = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __unicode__(self):
            return self.nom_court
