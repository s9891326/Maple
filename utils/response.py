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


def jsonify(data_status=0, data_msg='ok', results=None,
            http_status=None, **kwargs):
    encoded_data = json.dumps(dict(
        data_status=data_status,
        data_msg=data_msg,
        results=results,
        http_status=http_status,
        **kwargs),
        ensure_ascii=False,
    )
    
    return HttpResponse(
        encoded_data,
        content_type="application/json"
    )
