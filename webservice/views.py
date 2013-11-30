# -*- coding: utf8 -*-

import json
from json import encoder;

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.core import serializers

from perelachaise.models import Tombe

@require_http_methods(["GET"])
def tombe(request):
    """
    GET : renvoie la liste des tombes
    """
    
    queryset = Tombe.objects.all()
    list = []
    for row in queryset:
        list.append({
            'id': row.pk,
            'nom_court': row.nom_court,
            'latitude': row.latitude,
            'longitude': row.longitude
        })
    
    encoder.FLOAT_REPR = lambda o: format(o, '.6f')
    
    return HttpResponse(json.dumps({'tombes': list}, ensure_ascii=False), mimetype='application/json')
