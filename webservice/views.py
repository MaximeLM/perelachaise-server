# -*- coding: utf8 -*-

import json
import datetime
from decimal import Decimal

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from perelachaise.models import Monument

def toJsonString(obj):
    """ Convertit un objet python en représentation JSON """
    if obj == None:
        return ''
    elif isinstance(obj,datetime.date):
        return str(obj)
    elif isinstance(obj,Decimal):
        return str(obj)
    else:
        return obj


@require_http_methods(["GET"])
def monument_all(request):
    """
    GET : renvoie les monuments contrôlés
    Pas de paramètres
    """
    
    # Récupération de la liste des monuments contrôlés
    monuments = Monument.objects.filter(controle = 1)
    
    # Construction du résultat
    list = []
    for monument in monuments:
        # Monument
        monument_result = {
            'id': toJsonString(monument.pk),
            'nom': toJsonString(monument.nom),
            'nom_pour_tri': toJsonString(monument.nom_pour_tri),
            'code_wikipedia': toJsonString(monument.code_wikipedia),
            'resume': toJsonString(monument.resume),
        }
        
        # Node OSM
        node_osm = monument.node_osm
        monument_result['node_osm'] = {
            'id': toJsonString(node_osm.pk),
            'latitude': toJsonString(node_osm.latitude),
            'longitude': toJsonString(node_osm.longitude),
        }
        
        # Personnalites
        personnalites_result = []
        for personnalite in monument.personnalite_set.all():
            personnalites_result.append({
                'id': toJsonString(personnalite.pk),
                'nom': toJsonString(personnalite.nom),
                'code_wikipedia': toJsonString(personnalite.code_wikipedia),
                'activite': toJsonString(personnalite.activite),
                'resume': toJsonString(personnalite.resume),
                'date_naissance': toJsonString(personnalite.date_naissance),
                'date_naissance_precision': toJsonString(personnalite.date_naissance_precision),
                'date_deces': toJsonString(personnalite.date_deces),
                'date_deces_precision': toJsonString(personnalite.date_deces_precision),
            })
        
        monument_result['personnalites'] = personnalites_result
        
        list.append(monument_result)
    
    # Construction du contenu de la réponse
    content = json.dumps({'monuments': list}, ensure_ascii=False)
    
    # Renvoi de la réponse
    return HttpResponse(content, mimetype='application/json; charset=utf-8')
