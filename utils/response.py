import json

from django.http import HttpResponse
from rest_framework.response import Response


def common_finalize_response(finalize_response, request, response, *args, **kwargs):
    response = finalize_response(request, response, *args, **kwargs)
    response.data = dict(
        status=response.status_code,
        msg=response.status_text,
        result=response.data,
    )
    return response


def jsonify(results, status=0, msg='ok', **kwargs):
    encoded_data = json.dumps(dict(
        status=status,
        msg=msg,
        results=results,
        **kwargs),
        ensure_ascii=False,
    )
    
    return HttpResponse(
        encoded_data,
        content_type="application/json"
    )
