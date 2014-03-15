#!/usr/bin/env python
# encoding: utf-8

import datetime

from django.test import TestCase

from perelachaise.models import NodeOSM, Monument, Personnalite

class MonumentTest(TestCase):
    """
    Tests du modèle Monument
    """
    
    # Fixture
    fixtures = ['perelachaise.json']
    
    def test_create_resume(self):
        """
        La création d'un monument doit supprimer les \r du résumé.
        """
        # Création d'un node OSM
        node_osm = NodeOSM.objects.get(pk=470258150)
        node_osm.pk = 999999
        node_osm.save()
        
        # Création d'un monument
        monument = Monument.objects.get(nom=u'Jim Morrison')
        monument.pk = 999999
        monument.resume = u'ligne 1\r\nligne 2\nligne 3\rligne4'
        monument.node_osm = node_osm
        monument.save()
        
        # Vérification de la suppression des \r
        self.assertEqual(u'ligne 1\nligne 2\nligne 3ligne4',monument.resume)
    
    def test_save_resume(self):
        """
        La sauvegarde d'un monument doit supprimer les \r du résumé.
        """
        # Modification d'un monument
        monument = Monument.objects.get(nom=u'Jim Morrison')
        monument.resume = u'ligne 1\r\nligne 2\nligne 3\rligne4'
        monument.save()
        
        # Vérification de la suppression des \r
        self.assertEqual(u'ligne 1\nligne 2\nligne 3ligne4',monument.resume)

class PersonnaliteTest(TestCase):
    """
    Tests du modèle Personnalite
    """
    
    # Fixture
    fixtures = ['perelachaise.json']
    
    def test_create_resume(self):
        """
        La création d'une personnalité doit supprimer les \r du résumé.
        """
        # Création d'une personnalité
        personnalite = Personnalite.objects.get(nom=u'Jim Morrison')
        personnalite.pk = 999999
        personnalite.resume = u'ligne 1\r\nligne 2\nligne 3\rligne4'
        personnalite.save()
        
        # Vérification de la suppression des \r
        self.assertEqual(u'ligne 1\nligne 2\nligne 3ligne4',personnalite.resume)
    
    def test_save_resume(self):
        """
        La sauvegarde d'une personnalité doit supprimer les \r du résumé.
        """
        # Modification d'une personnalité
        personnalite = Personnalite.objects.get(nom=u'Jim Morrison')
        personnalite.resume = u'ligne 1\r\nligne 2\nligne 3\rligne4'
        personnalite.save()
        
        # Vérification de la suppression des \r
        self.assertEqual(u'ligne 1\nligne 2\nligne 3ligne4',personnalite.resume)
