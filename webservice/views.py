# -*- coding: utf8 -*-

import json
import datetime
import urllib2

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

def prepare_json_nodeOSM_for_monument_all(node_osm, extra):
    """ Renvoie un dictionnaire pour dump json correspondant à l'objet indiqué """
    result = {
            'id': to_json_string(node_osm.pk),
            'latitude': to_json_string(node_osm.latitude),
            'longitude': to_json_string(node_osm.longitude),
        }
    
    if extra:
        # Ajout du lien OpenStreetMap
        result['lien_openstreetmap'] = 'http://www.openstreetmap.org/node/%s' % node_osm.id
    
    return result

def prepare_json_imageCommons_for_monument_all(image_commons, extra):
    """ Renvoie un dictionnaire pour dump json correspondant à l'objet indiqué """
    result = {
            'id': to_json_string(image_commons.pk),
            'nom': to_json_string(image_commons.nom),
            'auteur': to_json_string(image_commons.auteur),
            'licence': to_json_string(image_commons.licence),
            'url_original': to_json_string(image_commons.url_original),
        }
    
    if extra:
        # Ajout du lien Wikimedia Commons
        result['lien_wikimedia_commons'] = 'http://commons.wikimedia.org/wiki/File:%s' % urllib2.quote(image_commons.nom.encode('utf8'))
    
    return result

def prepare_json_personnalite_for_monument_all(personnalite, extra):
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
    
    if extra:
        # Ajout des liens
        
        if personnalite.code_wikipedia != '':
            result['lien_wikipedia'] = 'http://fr.wikipedia.org/wiki/%s' % urllib2.quote(personnalite.code_wikipedia.encode('utf8'))
        else:
            result['lien_wikipedia'] = ''
        
        if personnalite.code_wikidata != '':
            result['lien_wikidata'] = 'http://www.wikidata.org/wiki/%s?uselang=fr' % urllib2.quote(personnalite.code_wikidata.encode('utf8'))
        else:
            result['lien_wikidata'] = ''
        
        if personnalite.categorie_commons != '':
            result['lien_categorie_wikimedia_commons'] = 'http://commons.wikimedia.org/wiki/Category:%s' % urllib2.quote(personnalite.categorie_commons.encode('utf8'))
        else:
            result['lien_categorie_wikimedia_commons'] = ''
    
    return result

def prepare_json_monument_for_monument_all(monument, extra):
    """ Renvoie un dictionnaire pour dump json correspondant à l'objet indiqué """
    # Monument
    result = {
        'id': to_json_string(monument.pk),
        'nom': to_json_string(monument.nom),
        'nom_pour_tri': to_json_string(monument.nom_pour_tri),
        'code_wikipedia': to_json_string(monument.code_wikipedia),
        'resume': to_json_string(monument.resume),
    }
    
    if extra:
        # Ajout des liens
        
        if monument.code_wikipedia != '':
            result['lien_wikipedia'] = 'http://fr.wikipedia.org/wiki/%s' % urllib2.quote(monument.code_wikipedia.encode('utf8'))
        else:
            result['lien_wikipedia'] = ''
        
        if monument.code_wikidata != '':
            result['lien_wikidata'] = 'http://www.wikidata.org/wiki/%s?uselang=fr' % urllib2.quote(monument.code_wikidata.encode('utf8'))
        else:
            result['lien_wikidata'] = ''
        
        if monument.categorie_commons != '':
            result['lien_categorie_wikimedia_commons'] = 'http://commons.wikimedia.org/wiki/Category:%s' % urllib2.quote(monument.categorie_commons.encode('utf8'))
        else:
            result['lien_categorie_wikimedia_commons'] = ''
    
    # Node OSM
    node_osm = monument.node_osm
    result['node_osm'] = prepare_json_nodeOSM_for_monument_all(node_osm, extra)
    
    # Image principale
    if monument.image_principale:
        result['image_principale'] = prepare_json_imageCommons_for_monument_all(monument.image_principale, extra)
    else:
        result['image_principale'] = None
    
    # Personnalites
    personnalites_result = []
    for personnalite in monument.personnalite_set.all().order_by('nom'):
        personnalites_result.append(prepare_json_personnalite_for_monument_all(personnalite, extra))
    
    result['personnalites'] = personnalites_result
    
    return result

@require_http_methods(["GET"])
def monument_all(request):
    """
    GET : renvoie les monuments contrôlés
    Paramètre optionnel : 'extra' - indique si le résultat doit contenir des champs additionnels
    """
    
    # Récupération de la valeur du paramètre extra
    extra = request.GET.has_key('extra') and request.GET['extra'] == '1'
    
    # Récupération de la liste des monuments contrôlés
    monuments = Monument.objects.filter(controle = 1).order_by('nom_pour_tri')
    
    # Construction du résultat
    list = []
    for monument in monuments:
        list.append(prepare_json_monument_for_monument_all(monument, extra))
    
    # Construction du contenu de la réponse
    content = dump_json({'monuments': list})
    
    # Renvoi de la réponse
    return HttpResponse(content, mimetype='application/json; charset=utf-8')
