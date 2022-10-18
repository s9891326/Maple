from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response

from utils import error_msg

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_one_week_ago():
    return timezone.localtime(timezone.now() - timezone.timedelta(days=7))


def common_finalize_response(finalize_response, request, response, *args, **kwargs):
    response = finalize_response(request, response, *args, **kwargs)
    response.data = dict(
        status=response.status_code,
        msg=response.status_text,
        result=response.data,
    )
    return response


def update_query_params(request, form):
    """
    透過form的方式來清理輸入的資料
    :param request:
    :param form:
    :return:
    """
    form = form(request.query_params)
    if form.is_valid():
        request.query_params._mutable = True
        clean_data = {k: v for k, v in form.clean().items() if v != "" and v is not None and k in form.data.keys()}
        request.query_params.clear()
        request.query_params.update(clean_data)
    else:
        return form.errors


class CustomModelViewSet(viewsets.ModelViewSet):
    # 如果有特殊的刪除需求，再進行override
    def destroy(self, request, *args, **kwargs):
        create_by = request.user
        instance = self.get_object()
        
        if hasattr(instance, 'create_by') and create_by != instance.create_by:
            return Response(error_msg.CREATE_BY_NOT_CORRECT, status=status.HTTP_400_BAD_REQUEST)
        
        return super().destroy(request, *args, **kwargs)
    
    def finalize_response(self, request, response, *args, **kwargs):
        return common_finalize_response(super().finalize_response, request, response, *args, **kwargs)
