# -*- coding: utf8 -*-

import json
from decimal import Decimal

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect, HttpResponseServerError
from django.views.decorators.http import require_http_methods
from django.core import serializers

from perelachaise.models import Monument, Personnalite, NodeOSM, ImageCommons
from webservice.views import dump_json, prepare_json_nodeOSM_for_monument_all, prepare_json_personnalite_for_monument_all, prepare_json_monument_for_monument_all

@require_http_methods(["GET"])
def fixtures_monumentall_nodeOSM(request, name):
    """
    Renvoie la fixture de Node OSM pour la vue monument/all/ correspondant au nom indiqué
    """
    
    if name == 'nodeOSM1':
        # Alphonse Daudet
        nodeOSM = NodeOSM.objects.get(pk=2663325709)
    elif name == 'nodeOSM1_update':
        # Alphonse Daudet modifié
        nodeOSM = NodeOSM.objects.get(pk=2663325709)
        nodeOSM.latitude = Decimal('42.4')
        nodeOSM.longitude = Decimal('-42.4')
    elif name == 'nodeOSM2':
        # Jim Morrison
        nodeOSM = NodeOSM.objects.get(pk=1915793663)
    elif name == 'nodeOSM2_update':
        # Jim Morrison modifié
        nodeOSM = NodeOSM.objects.get(pk=1915793663)
        nodeOSM.latitude = Decimal('42.48')
        nodeOSM.longitude = Decimal('0.0')
    else:
        return HttpResponseBadRequest()
        
    # Construction du résultat
    result = prepare_json_nodeOSM_for_monument_all(nodeOSM)
    
    return HttpResponse(dump_json(result), mimetype='application/json; charset=utf-8')

@require_http_methods(["GET"])
def fixtures_monumentall_personnalite(request, name):
    """
    Renvoie la fixture de personnalité pour la vue monument/all/ correspondant au nom indiqué
    """
    
    if name == 'personnalite1':
        # Jim Morrison
        personnalite = Personnalite.objects.get(pk=120)
    elif name == 'personnalite1_update':
        # Jim Morrison modifié UTF8
        personnalite = Personnalite.objects.get(pk=120)
        personnalite.nom = u'Jim Morrison ü'
        personnalite.activite = u'Activité'
        personnalite.resume = u'Résumé çê'
    elif name == 'personnalite2':
        # Téo Hernandez vide
        personnalite = Personnalite.objects.get(pk=194)
        personnalite.code_wikipedia = ''
        personnalite.activite = ''
        personnalite.resume = ''
        personnalite.date_naissance = None
        personnalite.date_deces = None
    elif name == 'personnalite2_update':
        # Téo Hernandez non vide
        personnalite = Personnalite.objects.get(pk=194)
    else:
        return HttpResponseBadRequest()
        
    # Construction du résultat
    result = prepare_json_personnalite_for_monument_all(personnalite)
    
    return HttpResponse(dump_json(result), mimetype='application/json; charset=utf-8')

@require_http_methods(["GET"])
def fixtures_monumentall_monument(request, name):
    """
    Renvoie la fixture de monument pour la vue monument/all/ correspondant au nom indiqué
    """
    
    # Chargement des objets
    
    monument1 = Monument.objects.get(pk=164)            # Mur des Fédérés (full + UTF8)
    monument2 = Monument.objects.get(pk=120)            # Jim Morrison (vide)
    monument3 = Monument.objects.get(pk=218)            # Édith Piaf
    
    nodeOSM1 = NodeOSM.objects.get(pk=2661217171)       # Jean de La Fontaine
    
    personnalite1 = Personnalite.objects.get(pk=207)    # Alain Bashung
    personnalite2 = Personnalite.objects.get(pk=76)     # Georges Courteline
    personnalite3 = Personnalite.objects.get(pk=120)    # Jim Morrison
    personnalite4 = Personnalite.objects.get(pk=231)    # François d'Astier de La Vigerie
    
    if name == 'monument1':
        monument = monument1
        
        # Construction du résultat
        result = prepare_json_monument_for_monument_all(monument)
        
        # Ajout d'une personnalité
        result_personnalite1 = prepare_json_personnalite_for_monument_all(personnalite1)
        result['personnalites'] = [result_personnalite1]
        
    elif name == 'monument1_update':
        monument = monument1
        
        # Update node OSM
        monument.node_osm.latitude = Decimal('42.4')
        monument.node_osm.longitude = Decimal('-42.4')
        
        # Suppression de l'image principale
        monument.image_principale = None
        
        # Construction du résultat
        result = prepare_json_monument_for_monument_all(monument)
        
        # Ajout d'une autre personnalité
        result_personnalite2 = prepare_json_personnalite_for_monument_all(personnalite2)
        result['personnalites'] = [result_personnalite2]
        
    elif name == 'monument2':
        monument = monument2
        
        # Suppression de l'image principale
        monument.image_principale = None
        
        # Construction du résultat
        result = prepare_json_monument_for_monument_all(monument)
        
        # Suppression des personnalités
        result['personnalites'] = []
        
    elif name == 'monument2_update1':
        monument = monument2
        
        # Modification de l'image principale
        monument.image_principale.nom = 'test_nom'
        monument.image_principale.auteur = 'test_auteur'
        monument.image_principale.licence = 'test_licence'
        monument.image_principale.url_original = 'test_url_original'
        
        # Construction du résultat
        result = prepare_json_monument_for_monument_all(monument)
        
        # Modification du node OSM
        result_nodeOSM1 = prepare_json_nodeOSM_for_monument_all(nodeOSM1)
        result['node_osm'] = result_nodeOSM1
        
    elif name == 'monument2_update2':
        monument = monument2
        
        # Remplacement de l'image principale
        monument.image_principale = monument3.image_principale
        
        # Construction du résultat
        result = prepare_json_monument_for_monument_all(monument)
        
        # Modification de la personnalité présente
        result_personnalite3 = prepare_json_personnalite_for_monument_all(personnalite3)
        result_personnalite3['nom'] = u'Nouveau nom'
        result_personnalite3['resume'] = u'Nouveau résumé'
        
        # Ajout d'une personnalité
        result_personnalite4 = prepare_json_personnalite_for_monument_all(personnalite4)
        
        result['personnalites'] = [result_personnalite3, result_personnalite4]
    
    elif name == 'monument3':
        monument = monument3
        
        # Construction du résultat
        result = prepare_json_monument_for_monument_all(monument)
        
        # Modification du nom
        result['nom_pour_tri'] = u'Édith'
        
    else:
        return HttpResponseBadRequest()
    
    return HttpResponse(dump_json(result), mimetype='application/json; charset=utf-8')

def monument_all(request):
    """
    Bouchon de la requête monument/all/
    """
    
    # Récupération du paramètre de la requête
    if not request.REQUEST.has_key('name'):
        name = '2_ok'
    else:
        name = request.REQUEST['name']
    
    if name == '1_ok':
        # Chargement des monuments
        monument1 = prepare_json_monument_for_monument_all(Monument.objects.get(pk=120))
        monument2 = prepare_json_monument_for_monument_all(Monument.objects.get(pk=164))
        monument3 = prepare_json_monument_for_monument_all(Monument.objects.get(pk=227))
        
        result = {'monuments': [monument1, monument2, monument3]}
        
    elif name == '2_ok':
        # Chargement des monuments
        monument1 = prepare_json_monument_for_monument_all(Monument.objects.get(pk=92))
        monument2 = prepare_json_monument_for_monument_all(Monument.objects.get(pk=120))
        
        result = {'monuments': [monument1, monument2]}
        
    elif name == '3_vide':
        result = {'monuments': []}
        
    elif name == '4_souscle':
        # Chargement des monuments
        monument1 = prepare_json_monument_for_monument_all(Monument.objects.get(pk=92))
        
        result = {'trucs': {'monuments': [monument1]}}
        
    elif name == '5_surcle':
        # Chargement des monuments
        monument1 = prepare_json_monument_for_monument_all(Monument.objects.get(pk=92))
        
        result = {'monuments': {'trucs': [monument1]}}
        
    elif name == '6_doublecle':
        # Chargement des monuments
        monument1 = prepare_json_monument_for_monument_all(Monument.objects.get(pk=92))
        
        result = {'monuments': {'monuments': [monument1]}}
        
    elif name == '7_autrecle':
        # Chargement des monuments
        monument1 = prepare_json_monument_for_monument_all(Monument.objects.get(pk=92))
        
        result = {'trucs': [monument1]}
        
    elif name == '8_404':
        # Chargement des monuments
        monument1 = prepare_json_monument_for_monument_all(Monument.objects.get(pk=92))
        monument2 = prepare_json_monument_for_monument_all(Monument.objects.get(pk=120))
        
        result = {'monuments': [monument1, monument2]}
        
        return HttpResponseNotFound(dump_json(result), mimetype='application/json; charset=utf-8')
        
    elif name == '9_500':
        # Chargement des monuments
        monument1 = prepare_json_monument_for_monument_all(Monument.objects.get(pk=92))
        monument2 = prepare_json_monument_for_monument_all(Monument.objects.get(pk=120))
        
        result = {'monuments': [monument1, monument2]}
        
        return HttpResponseServerError(dump_json(result), mimetype='application/json; charset=utf-8')
        
    else:
        return HttpResponseBadRequest()
    
    return HttpResponse(dump_json(result), mimetype='application/json; charset=utf-8')

def fixtures_test_webservice(request):
    """
    Renvoie la fixture du modèle django pour les tests du web service
    """
    # Récupération des monuments voulus
    monuments = [
        Monument.objects.get(pk=9),     # Alphonse Daudet
        Monument.objects.get(pk=76),    # Georges Courteline
        Monument.objects.get(pk=92),    # Henri Barbusse
        Monument.objects.get(pk=99),    # Isadora Duncan
        Monument.objects.get(pk=120),   # Jim Morrison
        Monument.objects.get(pk=164),   # Mur des Fédérés
        Monument.objects.get(pk=193),   # Abélard & Héloïse
        Monument.objects.get(pk=194),   # Téo Hernandez
        Monument.objects.get(pk=205),   # Alain Bashung
        Monument.objects.get(pk=218),   # Édith Piaf
        Monument.objects.get(pk=227),   # Famille d'Aboville
        Monument.objects.get(pk=228),   # François d'Astier de La Vigerie
        Monument.objects.get(pk=241),   # Jean de La Fontaine
    ]
    
    # Récupération des nodes OSM, personnalités et images Commons associés
    nodesOSM = []
    personnalites = []
    images_commons = []
    for monument in monuments:
        nodesOSM.append(monument.node_osm)
        images_commons.append(monument.image_principale)
        for personnalite in monument.personnalite_set.all():
            personnalites.append(personnalite)
    
    # Construction du résultat
    result = monuments
    result.extend(nodesOSM)
    result.extend(personnalites)
    result.extend(images_commons)
    return HttpResponse(serializers.serialize("json", result), mimetype='application/json; charset=utf-8')
