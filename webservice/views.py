# -*- coding: utf8 -*-

import json
import datetime
from decimal import Decimal

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from perelachaise.models import Monument

def to_json_string(obj):
    """ Convertit un objet python en représentation JSON """
    if obj == None:
        return ''
    elif isinstance(obj,datetime.date):
        return str(obj)
    elif isinstance(obj,Decimal):
        return str(obj)
    else:
        return obj

def dump_json(jsonObject):
    """ Convertit un objet python en JSON """
    return json.dumps(jsonObject, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True)

def prepare_json_nodeOSM_for_monument_all(node_osm):
    """ Renvoie un dictionnaire pour dump json correspondant à l'objet indiqué """
    result = {
            'id': to_json_string(node_osm.pk),
            'latitude': to_json_string(node_osm.latitude),
            'longitude': to_json_string(node_osm.longitude),
        }
    return result

def prepare_json_imageCommons_for_monument_all(image_commons):
    """ Renvoie un dictionnaire pour dump json correspondant à l'objet indiqué """
    result = {
            'id': to_json_string(image_commons.pk),
            'nom': to_json_string(image_commons.nom),
            'auteur': to_json_string(image_commons.auteur),
            'licence': to_json_string(image_commons.licence),
            'url_original': to_json_string(image_commons.url_original),
        }
    return result

def prepare_json_personnalite_for_monument_all(personnalite):
    """ Renvoie un dictionnaire pour dump json correspondant à l'objet indiqué """
    result = {
            'id': to_json_string(personnalite.pk),
            'nom': to_json_string(personnalite.nom),
            'code_wikipedia': to_json_string(personnalite.code_wikipedia),
            'activite': to_json_string(personnalite.activite),
            'resume': to_json_string(personnalite.resume),
            'date_naissance': to_json_string(personnalite.date_naissance),
            'date_naissance_precision': to_json_string(personnalite.date_naissance_precision),
            'date_deces': to_json_string(personnalite.date_deces),
            'date_deces_precision': to_json_string(personnalite.date_deces_precision),
        }
    return result

def prepare_json_monument_for_monument_all(monument):
    """ Renvoie un dictionnaire pour dump json correspondant à l'objet indiqué """
    # Monument
    result = {
        'id': to_json_string(monument.pk),
        'nom': to_json_string(monument.nom),
        'nom_pour_tri': to_json_string(monument.nom_pour_tri),
        'code_wikipedia': to_json_string(monument.code_wikipedia),
        'resume': to_json_string(monument.resume),
    }
    
    # Node OSM
    node_osm = monument.node_osm
    result['node_osm'] = prepare_json_nodeOSM_for_monument_all(node_osm)
    
    # Image principale
    if monument.image_principale:
        result['image_principale'] = prepare_json_imageCommons_for_monument_all(monument.image_principale)
    
    # Personnalites
    personnalites_result = []
    for personnalite in monument.personnalite_set.all().order_by('nom'):
        personnalites_result.append(prepare_json_personnalite_for_monument_all(personnalite))
    
    result['personnalites'] = personnalites_result
    
    return result

@require_http_methods(["GET"])
def monument_all(request):
    """
    GET : renvoie les monuments contrôlés
    Pas de paramètres
    """
    
    # Récupération de la liste des monuments contrôlés
    monuments = Monument.objects.filter(controle = 1).order_by('nom_pour_tri')
    
    # Construction du résultat
    list = []
    for monument in monuments:
        list.append(prepare_json_monument_for_monument_all(monument))
    
    # Construction du contenu de la réponse
    content = dump_json({'monuments': list})
    
    # Renvoi de la réponse
    return HttpResponse(content, mimetype='application/json; charset=utf-8')
