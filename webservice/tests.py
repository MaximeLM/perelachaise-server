#!/usr/bin/env python
# encoding: utf-8

import json
import time, datetime
from decimal import Decimal

from django.test import TestCase
from django.test.client import Client

from perelachaise.models import NodeOSM, Monument, Personnalite, ImageCommons
from webservice.views import to_json_string, prepare_json_nodeOSM_for_monument_all, prepare_json_personnalite_for_monument_all, prepare_json_monument_for_monument_all, prepare_json_imageCommons_for_monument_all

class MonumentAllTest(TestCase):
    """
    Tests de la vue monument/all/
    """
    
    # Fixture
    fixtures = ['perelachaise.json']
    
    def util_list_to_dict_result(self, monuments):
        """ Transforme une liste de monuments renvoyée par la requête en dictionnaire indexé sur le nom """
        
        # Préparation du résultat
        result = {}
        
        # Parcours des monuments
        for monument in monuments:
            # Récupération du nom
            nom = monument['nom']
            
            # Parcours des personnalités
            personnalites = {}
            for personnalite in monument['personnalites']:
                # Récupération du nom
                nom_personnalite = personnalite['nom']
                
                # Ajout au dictionnaire
                personnalites[nom_personnalite] = personnalite
            
            monument['personnalites'] = personnalites
            
            # Ajout au dictonnaire
            result[nom] = monument
        
        return result
    
    def assert_monument_equal(self, monument_json, monument_ref):
        """ Vérifie qu'un monument obtenu par requête est égal à un monument en base """
        
        # Vérification des champs du monument
        self.assertTrue(isinstance(monument_json, dict))
        
        # Id monument
        self.assertTrue(monument_json.has_key('id'))
        self.assertEqual(monument_ref.id, monument_json['id'])
        
        # Nom monument
        self.assertTrue(monument_json.has_key('nom'))
        self.assertEqual(monument_ref.nom, monument_json['nom'])
        
        # Nom pour tri monument
        self.assertTrue(monument_json.has_key('nom_pour_tri'))
        self.assertEqual(monument_ref.nom_pour_tri, monument_json['nom_pour_tri'])
        
        # Code wikipedia monument
        self.assertTrue(monument_json.has_key('code_wikipedia'))
        self.assertEqual(monument_ref.code_wikipedia, monument_json['code_wikipedia'])
        
        # Résumé monument
        self.assertTrue(monument_json.has_key('resume'))
        self.assertEqual(monument_ref.resume, monument_json['resume'])
        
        # Vérification des champs du node OSM
        self.assertTrue(monument_json.has_key('node_osm'))
        node_osm_json = monument_json['node_osm']
        node_osm_ref = monument_ref.node_osm
        self.assertTrue(isinstance(node_osm_json, dict))
        
        # Id node OSM
        self.assertTrue(node_osm_json.has_key('id'))
        self.assertEqual(node_osm_ref.id, node_osm_json['id'])
        
        # Latitude node OSM
        self.assertTrue(node_osm_json.has_key('latitude'))
        self.assertEqual(node_osm_ref.latitude, Decimal(node_osm_json['latitude']))
        
        # Longitude node OSM
        self.assertTrue(node_osm_json.has_key('longitude'))
        self.assertEqual(node_osm_ref.longitude, Decimal(node_osm_json['longitude']))
        
        if monument_ref.image_principale:
            # Vérification des champs de l'image principale
            self.assertTrue(monument_json.has_key('image_principale'))
            image_commons_json = monument_json['image_principale']
            image_commons_ref = monument_ref.image_principale
            self.assertTrue(isinstance(image_commons_json, dict))
        
            # Nom image Commons
            self.assertTrue(image_commons_json.has_key('nom'))
            self.assertEqual(image_commons_ref.nom, image_commons_json['nom'])
            
            # Auteur image Commons
            self.assertTrue(image_commons_json.has_key('auteur'))
            self.assertEqual(image_commons_ref.auteur, image_commons_json['auteur'])
            
            # Licence image Commons
            self.assertTrue(image_commons_json.has_key('licence'))
            self.assertEqual(image_commons_ref.licence, image_commons_json['licence'])
            
            # URL originale image Commons
            self.assertTrue(image_commons_json.has_key('url_original'))
            self.assertEqual(image_commons_ref.url_original, image_commons_json['url_original'])
        
        # Vérification des champs des personnalités
        self.assertTrue(monument_json.has_key('personnalites'))
        personnalites_json = monument_json['personnalites']
        
        # Parcours des personnalites
        for personnalite_ref in monument_ref.personnalite_set.all():
            
            # Vérification de la présence de la personnalité
            self.assertTrue(personnalites_json.has_key(personnalite_ref.nom))
            personnalite_json = personnalites_json[personnalite_ref.nom]
            
            # Vérification des champs de la personnalité
            self.assertTrue(isinstance(personnalite_json, dict))
        
            # Id personnalité
            self.assertTrue(personnalite_json.has_key('id'))
            self.assertEqual(personnalite_ref.id, personnalite_json['id'])
            
            # Nom personnalité
            self.assertTrue(personnalite_json.has_key('nom'))
            self.assertEqual(personnalite_ref.nom, personnalite_json['nom'])
            
            # Code wikipedia personnalité
            self.assertTrue(personnalite_json.has_key('code_wikipedia'))
            self.assertEqual(personnalite_ref.code_wikipedia, personnalite_json['code_wikipedia'])
            
            # Activité personnalité
            self.assertTrue(personnalite_json.has_key('activite'))
            self.assertEqual(personnalite_ref.activite, personnalite_json['activite'])
            
            # Résumé personnalité
            self.assertTrue(personnalite_json.has_key('resume'))
            self.assertEqual(personnalite_ref.resume, personnalite_json['resume'])
            
            # Date de naissance personnalité
            self.assertTrue(personnalite_json.has_key('date_naissance'))
            if personnalite_json['date_naissance'] != '':
                date_json = datetime.date(*time.strptime(personnalite_json['date_naissance'], "%Y-%m-%d")[:3])
            else:
                date_json = None
            self.assertEqual(personnalite_ref.date_naissance, date_json)
            
            # Précision date de naissance personnalité
            self.assertTrue(personnalite_json.has_key('date_naissance_precision'))
            self.assertEqual(personnalite_ref.date_naissance_precision, personnalite_json['date_naissance_precision'])
            
            # Date de décès personnalité
            self.assertTrue(personnalite_json.has_key('date_deces'))
            if personnalite_json['date_deces'] != '':
                date_json = datetime.date(*time.strptime(personnalite_json['date_deces'], "%Y-%m-%d")[:3])
            else:
                date_json = None
            self.assertEqual(personnalite_ref.date_deces, date_json)
            
            # Précision date de décès personnalité
            self.assertTrue(personnalite_json.has_key('date_deces_precision'))
            self.assertEqual(personnalite_ref.date_deces_precision, personnalite_json['date_deces_precision'])
    
    def test_get(self):
		"""
		Une requête au moyen de la méthode HTTP GET doit renvoyer un statut 'OK' (HTTP 200).
		"""
		# Requête avec GET
		response = self.client.get('/webservice/monument/all/')
		
		# Vérification du statut HTTP
		self.assertEqual(200, response.status_code)
        
		# Vérification du contenu de la réponse
		self.assertNotEqual('', response.content)
    
    def test_post(self):
		"""
		Une requête au moyen de la méthode HTTP POST doit renvoyer un statut 'Method Not Allowed' (HTTP 405).
		"""
		# Requête avec POST
		response = self.client.post('/webservice/monument/all/')
		
		# Vérification du statut HTTP
		self.assertEqual(405, response.status_code)
        
		# Vérification du contenu de la réponse
		self.assertEqual('', response.content)
    
    def test_put(self):
		"""
		Une requête au moyen de la méthode HTTP PUT doit renvoyer un statut 'Method Not Allowed' (HTTP 405).
		"""
		# Requête avec PUT
		response = self.client.post('/webservice/monument/all/')
		
		# Vérification du statut HTTP
		self.assertEqual(405, response.status_code)
        
		# Vérification du contenu de la réponse
		self.assertEqual('', response.content)
    
    def test_delete(self):
		"""
		Une requête au moyen de la méthode HTTP DELETE doit renvoyer un statut 'Method Not Allowed' (HTTP 405).
		"""
		# Requête de login avec DELETE
		response = self.client.post('/webservice/monument/all/')
		
		# Vérification du statut HTTP
		self.assertEqual(405, response.status_code)
        
		# Vérification du contenu de la réponse
		self.assertEqual('', response.content)
    
    def test_nodata(self):
        """
        Requête sans aucun monument présent en base
        """
        # Suppression des monuments
        Monument.objects.all().delete()
        
        # Requête avec GET
        response = self.client.get('/webservice/monument/all/')
        
        # Vérification du statut HTTP
        self.assertEqual(200, response.status_code)
        
        # Vérification du type de contenu
        self.assertEqual('application/json; charset=utf-8', response['Content-Type'])
        
        # Parcours des objets reçus
        jsonObject = json.loads(response.content)
        self.assertTrue(isinstance(jsonObject, dict))
        
        # Vérification de la présence de la liste de monuments
        self.assertTrue(jsonObject.has_key('monuments'))
        monuments = jsonObject['monuments'];
        self.assertTrue(isinstance(monuments, list))
        
        # Vérification du nombre d'objets reçus
        self.assertEqual(0, len(monuments))
    
    def test_1_personnalite(self):
        """
        Teste un monument auquel est associée une personnalité.
        """
        
        monument_ref = Monument.objects.get(nom = u'Jim Morrison')
        self.assertEqual(1, monument_ref.personnalite_set.count())
        
        # Requête avec GET
        response = self.client.get('/webservice/monument/all/')
        
        # Vérification du statut HTTP
        self.assertEqual(200, response.status_code)
        
        # Vérification du type de contenu
        self.assertEqual('application/json; charset=utf-8', response['Content-Type'])
        
        # Parcours des objets reçus
        jsonObject = json.loads(response.content)
        self.assertTrue(isinstance(jsonObject, dict))
        
        # Vérification de la présence de la liste de monuments
        self.assertTrue(jsonObject.has_key('monuments'))
        monuments = jsonObject['monuments'];
        self.assertTrue(isinstance(monuments, list))
        
        # Récupération du dictionnaire des monuments
        dict_monuments = self.util_list_to_dict_result(monuments)
        
        # Vérification de la présence du monument de référence
        self.assertTrue(dict_monuments.has_key(monument_ref.nom))
        monument_json = dict_monuments[monument_ref.nom]
        
        # Vérification du contenu du monument
        self.assert_monument_equal(monument_json, monument_ref)
    
    def test_2_personnalites(self):
        """
        Teste un monument auquel sont associées deux personnalités.
        """
        
        monument_ref = Monument.objects.get(nom = u'Tombeau d\'Abélard et Héloïse')
        self.assertEqual(2, monument_ref.personnalite_set.count())
        
        # Requête avec GET
        response = self.client.get('/webservice/monument/all/')
        
        # Vérification du statut HTTP
        self.assertEqual(200, response.status_code)
        
        # Vérification du type de contenu
        self.assertEqual('application/json; charset=utf-8', response['Content-Type'])
        
        # Parcours des objets reçus
        jsonObject = json.loads(response.content)
        self.assertTrue(isinstance(jsonObject, dict))
        
        # Vérification de la présence de la liste de monuments
        self.assertTrue(jsonObject.has_key('monuments'))
        monuments = jsonObject['monuments'];
        self.assertTrue(isinstance(monuments, list))
        
        # Récupération du dictionnaire des monuments
        dict_monuments = self.util_list_to_dict_result(monuments)
        
        # Vérification de la présence du monument de référence
        self.assertTrue(dict_monuments.has_key(monument_ref.nom))
        monument_json = dict_monuments[monument_ref.nom]
        
        # Vérification du contenu du monument
        self.assert_monument_equal(monument_json, monument_ref)
    
    def test_3_personnalites(self):
        """
        Teste un monument auquel sont associées trois personnalités.
        """
        
        monument_ref = Monument.objects.get(nom = u'Famille d\'Aboville')
        self.assertEqual(3, monument_ref.personnalite_set.count())
        
        # Requête avec GET
        response = self.client.get('/webservice/monument/all/')
        
        # Vérification du statut HTTP
        self.assertEqual(200, response.status_code)
        
        # Vérification du type de contenu
        self.assertEqual('application/json; charset=utf-8', response['Content-Type'])
        
        # Parcours des objets reçus
        jsonObject = json.loads(response.content)
        self.assertTrue(isinstance(jsonObject, dict))
        
        # Vérification de la présence de la liste de monuments
        self.assertTrue(jsonObject.has_key('monuments'))
        monuments = jsonObject['monuments'];
        self.assertTrue(isinstance(monuments, list))
        
        # Récupération du dictionnaire des monuments
        dict_monuments = self.util_list_to_dict_result(monuments)
        
        # Vérification de la présence du monument de référence
        self.assertTrue(dict_monuments.has_key(monument_ref.nom))
        monument_json = dict_monuments[monument_ref.nom]
        
        # Vérification du contenu du monument
        self.assert_monument_equal(monument_json, monument_ref)
    
    def test_champs_vides(self):
        """
        Teste un monument auquel est associée une personnalité et pour lequel tous les champs possibles sont vides.
        """
        
        monument_ref = Monument.objects.get(nom = u'Téo Hernandez')
        
        # Mise à vide ou None des champs quand possible
        monument_ref.code_wikipedia = ''
        monument_ref.resume = ''
        
        image_commons_ref = monument_ref.image_principale
        image_commons_ref.auteur = ''
        image_commons_ref.licence = ''
        image_commons_ref.url_originale = ''
        
        image_commons_ref.save()
        
        for personnalite_ref in monument_ref.personnalite_set.all():
            personnalite_ref.code_wikipedia = ''
            personnalite_ref.activite = ''
            personnalite_ref.resume = ''
            personnalite_ref.date_naissance = None
            personnalite_ref.date_deces = None
            
            personnalite_ref.save()
        
        monument_ref.save()
        
        # Requête avec GET
        response = self.client.get('/webservice/monument/all/')
        
        # Vérification du statut HTTP
        self.assertEqual(200, response.status_code)
        
        # Vérification du type de contenu
        self.assertEqual('application/json; charset=utf-8', response['Content-Type'])
        
        # Parcours des objets reçus
        jsonObject = json.loads(response.content)
        self.assertTrue(isinstance(jsonObject, dict))
        
        # Vérification de la présence de la liste de monuments
        self.assertTrue(jsonObject.has_key('monuments'))
        monuments = jsonObject['monuments'];
        self.assertTrue(isinstance(monuments, list))
        
        # Récupération du dictionnaire des monuments
        dict_monuments = self.util_list_to_dict_result(monuments)
        
        # Vérification de la présence du monument de référence
        self.assertTrue(dict_monuments.has_key(monument_ref.nom))
        monument_json = dict_monuments[monument_ref.nom]
        
        # Vérification du contenu du monument
        self.assert_monument_equal(monument_json, monument_ref)
    
    def test_avant_1900(self):
        """
        Teste un monument auquel est associée une personnalité dont les dates de naissance et de décès sont inférieures à 1900.
        Testé à cause d'une limitation des bibliothèques Python.
        """
        
        monument_ref = Monument.objects.get(nom = u'François d\'Astier de La Vigerie')
        
        # Modification des dates de la personnalité
        for personnalite_ref in monument_ref.personnalite_set.all():
            personnalite_ref.date_naissance = datetime.date(1645,10,15)
            personnalite_ref.date_deces = datetime.date(1745,10,15)
            
            personnalite_ref.save()
        
        # Requête avec GET
        response = self.client.get('/webservice/monument/all/')
        
        # Vérification du statut HTTP
        self.assertEqual(200, response.status_code)
        
        # Vérification du type de contenu
        self.assertEqual('application/json; charset=utf-8', response['Content-Type'])
        
        # Parcours des objets reçus
        jsonObject = json.loads(response.content)
        self.assertTrue(isinstance(jsonObject, dict))
        
        # Vérification de la présence de la liste de monuments
        self.assertTrue(jsonObject.has_key('monuments'))
        monuments = jsonObject['monuments'];
        self.assertTrue(isinstance(monuments, list))
        
        # Récupération du dictionnaire des monuments
        dict_monuments = self.util_list_to_dict_result(monuments)
        
        # Vérification de la présence du monument de référence
        self.assertTrue(dict_monuments.has_key(monument_ref.nom))
        monument_json = dict_monuments[monument_ref.nom]
        
        # Vérification du contenu du monument
        self.assert_monument_equal(monument_json, monument_ref)
    
    def test_no_image_principale(self):
        """
        Teste un monument qui n'a pas d'image Commons associée.
        """
        
        monument_ref = Monument.objects.get(nom = u'Jim Morrison')
        
        # Suppression de l'image principale
        monument_ref.image_principale = None
        monument_ref.save()
        
        # Requête avec GET
        response = self.client.get('/webservice/monument/all/')
        
        # Vérification du statut HTTP
        self.assertEqual(200, response.status_code)
        
        # Vérification du type de contenu
        self.assertEqual('application/json; charset=utf-8', response['Content-Type'])
        
        # Parcours des objets reçus
        jsonObject = json.loads(response.content)
        self.assertTrue(isinstance(jsonObject, dict))
        
        # Vérification de la présence de la liste de monuments
        self.assertTrue(jsonObject.has_key('monuments'))
        monuments = jsonObject['monuments'];
        self.assertTrue(isinstance(monuments, list))
        
        # Récupération du dictionnaire des monuments
        dict_monuments = self.util_list_to_dict_result(monuments)
        
        # Vérification de la présence du monument de référence
        self.assertTrue(dict_monuments.has_key(monument_ref.nom))
        monument_json = dict_monuments[monument_ref.nom]
        
        # Vérification du contenu du monument
        self.assert_monument_equal(monument_json, monument_ref)
    
    def test_non_controle(self):
        """
        Vérifie qu'un monument non contrôlé n'est pas renvoyé.
        """
        
        monument_ref = Monument.objects.get(nom = u'Isadora Duncan')
        
        # Modification en base
        monument_ref.controle = 0
        monument_ref.save()
        
        # Requête avec GET
        response = self.client.get('/webservice/monument/all/')
        
        # Vérification du statut HTTP
        self.assertEqual(200, response.status_code)
        
        # Vérification du type de contenu
        self.assertEqual('application/json; charset=utf-8', response['Content-Type'])
        
        # Parcours des objets reçus
        jsonObject = json.loads(response.content)
        self.assertTrue(isinstance(jsonObject, dict))
        
        # Vérification de la présence de la liste de monuments
        self.assertTrue(jsonObject.has_key('monuments'))
        monuments = jsonObject['monuments'];
        self.assertTrue(isinstance(monuments, list))
        
        # Récupération du dictionnaire des monuments
        dict_monuments = self.util_list_to_dict_result(monuments)
        
        # Vérification de la non présence du monument de référence
        self.assertFalse(dict_monuments.has_key(monument_ref.nom))
    
    def test_all_nodata(self):
        """
        Requête avec tous les monuments non contrôlés
        """
        
        # Passage au statut non contrôlé de tous les monuments
        Monument.objects.all().update(controle=0); 
        
        # Requête avec GET
        response = self.client.get('/webservice/monument/all/')
        
        # Vérification du statut HTTP
        self.assertEqual(200, response.status_code)
        
        # Vérification du type de contenu
        self.assertEqual('application/json; charset=utf-8', response['Content-Type'])
        
        # Parcours des objets reçus
        jsonObject = json.loads(response.content)
        self.assertTrue(isinstance(jsonObject, dict))
        
        # Vérification de la présence de la liste de monuments
        self.assertTrue(jsonObject.has_key('monuments'))
        monuments = jsonObject['monuments'];
        self.assertTrue(isinstance(monuments, list))
        
        # Vérification du nombre d'objets reçus
        self.assertEqual(0, len(monuments))
    
    def test_to_json_string_none(self):
        """
        Un objet None doit être converti en chaîne de caractères vide.
        """
        self.assertEqual('',to_json_string(None))
    
    def test_to_json_string_string(self):
        """
        String
        """
        test = 'test'
        self.assertEqual(test,to_json_string(test))
    
    def test_to_json_string_utf8(self):
        """
        String UTF8
        """
        test = u'Testé'
        self.assertEqual(test,to_json_string(test))
    
    def test_to_json_string_date(self):
        """
        Date + heure
        """
        date = datetime.date.today()
        self.assertEqual(str(date),to_json_string(date))
    
    def test_to_json_string_decimal(self):
        """
        Décimal
        """
        decimal = Decimal(42)
        self.assertEqual(str(decimal),to_json_string(decimal))
    
    def test_prepare_json_nodeOSM_for_monument_all(self):
        """
        Préparation json d'un node OSM
        """
        nodeOSM = NodeOSM.objects.get(pk=2663325709)
        nodeOSM_json = prepare_json_nodeOSM_for_monument_all(nodeOSM)
        
        self.assertEqual(nodeOSM.id, nodeOSM_json['id'])
        self.assertEqual(nodeOSM.latitude, Decimal(nodeOSM_json['latitude']))
        self.assertEqual(nodeOSM.longitude, Decimal(nodeOSM_json['longitude']))
    
    def test_prepare_json_personnalite_for_monument_all_full(self):
        """
        Préparation json d'une personnalité (cas où tous les champs sont remplis)
        """
        personnalite = Personnalite.objects.get(pk=120)
        personnalite_json = prepare_json_personnalite_for_monument_all(personnalite)
        
        self.assertEqual(personnalite.id, personnalite_json['id'])
        self.assertEqual(personnalite.nom, personnalite_json['nom'])
        self.assertEqual(personnalite.code_wikipedia, personnalite_json['code_wikipedia'])
        self.assertEqual(personnalite.activite, personnalite_json['activite'])
        self.assertEqual(personnalite.resume, personnalite_json['resume'])
        self.assertEqual(personnalite.date_naissance, datetime.date(*time.strptime(personnalite_json['date_naissance'], "%Y-%m-%d")[:3]))
        self.assertEqual(personnalite.date_deces, datetime.date(*time.strptime(personnalite_json['date_deces'], "%Y-%m-%d")[:3]))
        self.assertEqual(personnalite.date_naissance_precision, personnalite_json['date_naissance_precision'])
        self.assertEqual(personnalite.date_deces_precision, personnalite_json['date_deces_precision'])
    
    def test_prepare_json_personnalite_for_monument_all_empty(self):
        """
        Préparation json d'une personnalité (cas où tous les champs possibles sont vides)
        """
        personnalite = Personnalite.objects.get(pk=120)
        personnalite.code_wikipedia = ''
        personnalite.activite = ''
        personnalite.resume = ''
        personnalite.date_naissance = ''
        personnalite.date_deces = ''
        personnalite_json = prepare_json_personnalite_for_monument_all(personnalite)
        
        self.assertEqual(personnalite.id, personnalite_json['id'])
        self.assertEqual(personnalite.nom, personnalite_json['nom'])
        self.assertEqual(personnalite.code_wikipedia, personnalite_json['code_wikipedia'])
        self.assertEqual(personnalite.activite, personnalite_json['activite'])
        self.assertEqual(personnalite.resume, personnalite_json['resume'])
        self.assertEqual('', personnalite_json['date_naissance'])
        self.assertEqual('', personnalite_json['date_deces'])
        self.assertEqual(personnalite.date_naissance_precision, personnalite_json['date_naissance_precision'])
        self.assertEqual(personnalite.date_deces_precision, personnalite_json['date_deces_precision'])
    
    def test_prepare_json_monument_for_monument_all(self):
        """
        Préparation json d'un monument
        """
        monument = Monument.objects.get(nom = u'Famille d\'Aboville')
        monument_json = prepare_json_monument_for_monument_all(monument)
        
        # Parcours des personnalités
        personnalites = {}
        for personnalite in monument_json['personnalites']:
            # Récupération du nom
            nom_personnalite = personnalite['nom']
            
            # Ajout au dictionnaire
            personnalites[nom_personnalite] = personnalite
        
        monument_json['personnalites'] = personnalites
        
        self.assert_monument_equal(monument_json, monument)
    
    def test_prepare_json_image_commons_for_monument_all_full(self):
        """
        Préparation json d'une image Commons où tous les champs sont remplis
        """
        image_commons = ImageCommons.objects.get(pk=129)
        image_commons_json = prepare_json_imageCommons_for_monument_all(image_commons)
        
        self.assertEqual(image_commons.nom, image_commons_json['nom'])
        self.assertEqual(image_commons.auteur, image_commons_json['auteur'])
        self.assertEqual(image_commons.licence, image_commons_json['licence'])
        self.assertEqual(image_commons.url_original, image_commons_json['url_original'])
    
    def test_prepare_json_image_commons_for_monument_all_empty(self):
        """
        Préparation json d'une image Commons où tous les champs optionnels sont vides
        """
        image_commons = ImageCommons.objects.get(pk=129)
        
        image_commons.auteur = ''
        image_commons.licence = ''
        image_commons.url_original = ''
        
        image_commons_json = prepare_json_imageCommons_for_monument_all(image_commons)
        
        self.assertEqual(image_commons.nom, image_commons_json['nom'])
        self.assertEqual('', image_commons_json['auteur'])
        self.assertEqual('', image_commons_json['licence'])
        self.assertEqual('', image_commons_json['url_original'])
