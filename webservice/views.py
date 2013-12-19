# -*- coding: utf8 -*-

import json
import datetime
from json import encoder

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.core import serializers

from perelachaise.models import Tombe

def toJsonString(obj):
    if obj == None:
        return ''
    elif isinstance(obj,datetime.date):
        return str(obj)
    else:
        return obj

@require_http_methods(["GET"])
def tombe(request):
    """
    GET : renvoie la liste des tombes
    """
    
    queryset = Tombe.objects.all()
    list = []
    for row in queryset:
        list.append({
            'id': toJsonString(row.pk),
            'nom_osm': toJsonString(row.nom_osm),
            'latitude': toJsonString(row.latitude),
            'longitude': toJsonString(row.longitude),
            'nom': toJsonString(row.nom),
            'prenom': toJsonString(row.prenom),
            'date_naissance': toJsonString(row.date_naissance),
            'date_deces': toJsonString(row.date_deces),
            'activite': toJsonString(row.activite),
            'resume': toJsonString(row.resume),
            'url_wikipedia': toJsonString(row.url_wikipedia)
        })
    
    encoder.FLOAT_REPR = lambda o: format(o, '.6f')
    
    return HttpResponse(json.dumps({'tombes': list}, ensure_ascii=False), mimetype='application/json')
