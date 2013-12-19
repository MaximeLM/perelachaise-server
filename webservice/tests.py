#!/usr/bin/env python
# encoding: utf-8

import json

from django.test import TestCase
from django.test.client import Client

from perelachaise.models import Tombe

class TombeTest(TestCase):
    """
    Tests de la vue tombe/
    """
    
    def test_post(self):
		"""
		Une connexion au moyen de la méthode HTTP POST doit renvoyer un statut 'Method Not Allowed' (HTTP 405).
		"""
		# Requête avec POST
		response = self.client.post('/webservice/tombe/')
		
		# Vérification du statut HTTP
		self.assertEqual(405, response.status_code)
        
		# Vérification du contenu de la réponse
		self.assertEqual('', response.content)
    
    def test_put(self):
		"""
		Une connexion au moyen de la méthode HTTP PUT doit renvoyer un statut 'Method Not Allowed' (HTTP 405).
		"""
		# Requête avec PUT
		response = self.client.put('/webservice/tombe/')
		
		# Vérification du statut HTTP
		self.assertEqual(405, response.status_code)
        
		# Vérification du contenu de la réponse
		self.assertEqual('', response.content)
    
    def test_delete(self):
		"""
		Une connexion au moyen de la méthode HTTP DELETE doit renvoyer un statut 'Method Not Allowed' (HTTP 405).
		"""
		# Requête de login avec DELETE
		response = self.client.delete('/webservice/tombe/')
		
		# Vérification du statut HTTP
		self.assertEqual(405, response.status_code)
        
		# Vérification du contenu de la réponse
		self.assertEqual('', response.content)
    
    def test_nodata(self):
        """
        Avec aucune tombe en base, le retour doit être vide.
        """
        # Requête de la liste des tombes
        response = self.client.get('/webservice/tombe/')
        
        # Vérification du statut HTTP
        self.assertEqual(200, response.status_code)
        
        # Vérification du type de contenu
        self.assertEqual('application/json', response['Content-Type'])
        
        # Parcours des objets reçus
        jsonObject = json.loads(response.content)
        self.assertTrue(isinstance(jsonObject, dict))
        
        # Vérification de la présence de la liste de tombes
        self.assertTrue(jsonObject.has_key('tombes'))
        tombes = jsonObject['tombes'];
        self.assertTrue(isinstance(tombes, list))
        
        # Vérification du nombre d'objets reçus
        self.assertEqual(0, len(tombes))
    
    def test_1object(self):
        """
        Avec 1 tombe en base.
        """
        # Préparation des données
        Tombe(pk=179, nom_osm=u'test1', latitude=0.0, longitude=1.0, nom=u'nom1', prenom=u'prénom1', date_naissance='1985-10-20', date_deces='1985-10-21', activite=u'activité1', resume=u'résumé1', url_wikipedia=u'http://test1.fr').save()
        
        # Requête de la liste des tombes
        response = self.client.get('/webservice/tombe/')
        
        # Vérification du statut HTTP
        self.assertEqual(200, response.status_code)
        
        # Vérification du type de contenu
        self.assertEqual('application/json', response['Content-Type'])
        
        # Parcours des objets reçus
        jsonObject = json.loads(response.content)
        self.assertTrue(isinstance(jsonObject, dict))
        
        # Vérification de la présence de la liste de tombes
        self.assertTrue(jsonObject.has_key('tombes'))
        tombes = jsonObject['tombes'];
        self.assertTrue(isinstance(tombes, list))
        
        # Vérification du nombre d'objets reçus
        self.assertEqual(1, len(tombes))
        
        # Récupération de l'objet tombe
        tombe = tombes[0];
        self.assertTrue(isinstance(tombe, dict))
        
        # Vérification de la présence de l'identifiant
        self.assertTrue(tombe.has_key('id'))
        self.assertEqual(179, tombe['id'])
        
        # Nom court
        self.assertTrue(tombe.has_key('nom_osm'))
        self.assertEqual(u'test1', tombe['nom_osm'])
        
        # Latitude
        self.assertTrue(tombe.has_key('latitude'))
        self.assertEqual(0.0, tombe['latitude'])
        
        # Longitude
        self.assertTrue(tombe.has_key('longitude'))
        self.assertEqual(1.0, tombe['longitude'])
        
        # Nom
        self.assertTrue(tombe.has_key('nom'))
        self.assertEqual(u'nom1', tombe['nom'])
        
        # Prénom
        self.assertTrue(tombe.has_key('prenom'))
        self.assertEqual(u'prénom1', tombe['prenom'])
        
        # Date de naissance
        self.assertTrue(tombe.has_key('date_naissance'))
        self.assertEqual('1985-10-20', tombe['date_naissance'])
        
        # Date de décès
        self.assertTrue(tombe.has_key('date_deces'))
        self.assertEqual('1985-10-21', tombe['date_deces'])
        
        # Activité
        self.assertTrue(tombe.has_key('activite'))
        self.assertEqual(u'activité1', tombe['activite'])
        
        # Résumé
        self.assertTrue(tombe.has_key('resume'))
        self.assertEqual(u'résumé1', tombe['resume'])
        
        # URL wikipedia
        self.assertTrue(tombe.has_key('url_wikipedia'))
        self.assertEqual(u'http://test1.fr', tombe['url_wikipedia'])
    
    def test_2objects(self):
        """
        Avec 2 tombes en base.
        """
        # Préparation des données
        Tombe(pk=1, nom_osm=u'tété', latitude=-96, longitude=0.123456, nom=u'nom1', prenom=u'prénom1', date_naissance='1985-10-20', date_deces='1985-10-21', activite=u'activité1', resume=u'résumé1', url_wikipedia=u'http://test1.fr').save()
        Tombe(pk=999, nom_osm=u'toto', latitude=96, longitude=3.123456, nom=u'nom2', prenom=u'', activite=u'', resume=u'', url_wikipedia=u'').save()
        
        # Requête de la liste des tombes
        response = self.client.get('/webservice/tombe/')
        
        # Vérification du statut HTTP
        self.assertEqual(200, response.status_code)
        
        # Vérification du type de contenu
        self.assertEqual('application/json', response['Content-Type'])
        
        # Parcours des objets reçus
        jsonObject = json.loads(response.content)
        self.assertTrue(isinstance(jsonObject, dict))
        
        # Vérification de la présence de la liste de tombes
        self.assertTrue(jsonObject.has_key('tombes'))
        tombes = jsonObject['tombes'];
        self.assertTrue(isinstance(tombes, list))
        
        # Vérification du nombre d'objets reçus
        self.assertEqual(2, len(tombes))
        
        # Parcours des objets tombes
        # Pas d'assertion sur l'ordre des tombes
        tombe1 = False;
        tombe2 = False;
        for i in range(2):
            # Récupération de la tombe
            tombe = tombes[i];
            self.assertTrue(isinstance(tombe, dict))
            
            # Vérification de la présence de l'identifiant
            self.assertTrue(tombe.has_key('id'))
            
            if tombe['id'] == 1:
                # Cas de la tombe 1
                tombe1 = True;
        
                # Nom court
                self.assertTrue(tombe.has_key('nom_osm'))
                self.assertEqual(u'tété', tombe['nom_osm'])
                
                # Latitude
                self.assertTrue(tombe.has_key('latitude'))
                self.assertEqual(-96, tombe['latitude'])
        
                # Longitude
                self.assertTrue(tombe.has_key('longitude'))
                self.assertEqual(0.123456, tombe['longitude'])
                
                # Nom
                self.assertTrue(tombe.has_key('nom'))
                self.assertEqual(u'nom1', tombe['nom'])
        
                # Prénom
                self.assertTrue(tombe.has_key('prenom'))
                self.assertEqual(u'prénom1', tombe['prenom'])
        
                # Date de naissance
                self.assertTrue(tombe.has_key('date_naissance'))
                self.assertEqual('1985-10-20', tombe['date_naissance'])
        
                # Date de décès
                self.assertTrue(tombe.has_key('date_deces'))
                self.assertEqual('1985-10-21', tombe['date_deces'])
        
                # Activité
                self.assertTrue(tombe.has_key('activite'))
                self.assertEqual(u'activité1', tombe['activite'])
        
                # Résumé
                self.assertTrue(tombe.has_key('resume'))
                self.assertEqual(u'résumé1', tombe['resume'])
        
                # URL wikipedia
                self.assertTrue(tombe.has_key('url_wikipedia'))
                self.assertEqual(u'http://test1.fr', tombe['url_wikipedia'])
        
            elif tombe['id'] == 999:
                # Cas de la tombe 2
                tombe2 = True;
                
                # Nom court
                self.assertTrue(tombe.has_key('nom_osm'))
                self.assertEqual(u'toto', tombe['nom_osm'])
                
                # Latitude
                self.assertTrue(tombe.has_key('latitude'))
                self.assertEqual(96, tombe['latitude'])
        
                # Longitude
                self.assertTrue(tombe.has_key('longitude'))
                self.assertEqual(3.123456, tombe['longitude'])
                
                # Nom
                self.assertTrue(tombe.has_key('nom'))
                self.assertEqual(u'nom2', tombe['nom'])
        
                # Prénom
                self.assertTrue(tombe.has_key('prenom'))
                self.assertEqual(u'', tombe['prenom'])
        
                # Date de naissance
                self.assertTrue(tombe.has_key('date_naissance'))
                self.assertEqual('', tombe['date_naissance'])
        
                # Date de décès
                self.assertTrue(tombe.has_key('date_deces'))
                self.assertEqual('', tombe['date_deces'])
        
                # Activité
                self.assertTrue(tombe.has_key('activite'))
                self.assertEqual(u'', tombe['activite'])
        
                # Résumé
                self.assertTrue(tombe.has_key('resume'))
                self.assertEqual(u'', tombe['resume'])
        
                # URL wikipedia
                self.assertTrue(tombe.has_key('url_wikipedia'))
                self.assertEqual(u'', tombe['url_wikipedia'])
                
            else:
                # Identifiant de tombe non attendu
                self.fail();
        
        # Vérification de la présence de toutes les tombes attendues
        if not tombe1 or not tombe2:
            self.fail();
