from rest_framework.renderers import JSONRenderer
from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.views import set_rollback
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils import six
from django.utils.translation import ugettext_lazy as _


class AotoPackRender(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, dict) and data.get('success_status', None) is False:
            pass
        else:
            data = {
                'success_status': True,
                'message': '',
                'data': data
            }
        return super(AotoPackRender, self).render(data, accepted_media_type, renderer_context)


def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    data = {
        'success_status': False
    }
    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        message = exc.detail
        if isinstance(exc, ValidationError) and isinstance(exc.detail, dict):
            for k, v in exc.detail.items():
                message = v[0]
                break

        if isinstance(exc.detail, list):
            message = exc.detail[0]

        data['message'] = message

        if isinstance(exc, exceptions.NotAuthenticated):
            data['permission'] = 401
        else:
            data['permission'] = exc.status_code

        set_rollback()
        return Response(data, status=status.HTTP_200_OK, headers=headers)

    elif isinstance(exc, Http404):
        msg = _('Not found.')
        data['message'] = six.text_type(msg)
        data['permission'] = 404

        set_rollback()
        return Response(data, status=status.HTTP_200_OK)

    elif isinstance(exc, PermissionDenied):
        msg = _('Permission denied.')
        data['message'] = six.text_type(msg)
        data['permission'] = 401

        set_rollback()
        return Response(data, status=status.HTTP_200_OK)

    return None
