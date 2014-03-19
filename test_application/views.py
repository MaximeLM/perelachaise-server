# -*- coding: utf8 -*-

import json
from decimal import Decimal

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods

from perelachaise.models import Monument, Personnalite, NodeOSM
from webservice.views import prepare_json_nodeOSM_for_monument_all, dump_json, prepare_json_personnalite_for_monument_all

@require_http_methods(["GET"])
def monumentall_nodeOSM(request, name):
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
def monumentall_personnalite(request, name):
    """
    Renvoie la fixture de personnalité pour la vue monument/all/ correspondant au nom indiqué
    """
    print name
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
