# -*- coding: utf8 -*-

import json
from decimal import Decimal

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods

from perelachaise.models import Monument, Personnalite, NodeOSM
from webservice.views import prepare_json_nodeOSM_for_monument_all, dump_json

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
    else:
        return HttpResponseBadRequest()
        
    # Construction du résultat
    result = prepare_json_nodeOSM_for_monument_all(nodeOSM)
    
    return HttpResponse(dump_json(result), mimetype='application/json; charset=utf-8')
