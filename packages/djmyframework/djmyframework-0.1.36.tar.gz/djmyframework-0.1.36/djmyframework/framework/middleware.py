# -*- coding: utf-8 -*-
import copy
import logging
import sys
import time

from django.http import Http404, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import exceptions, status
from rest_framework.exceptions import ValidationError
from rest_framework.views import set_rollback
import typing
from settings import DEBUG, LANGUAGE_CODE
from .response import Response, RspData
from .request import MyRequest
from .utils import json_dumps, trace_msg

import datetime
from objectdict import ObjectDict

_log = logging.getLogger('root')


class CustomRequest(MyRequest):
    """只是用作类型提示"""
    is_debug: bool
    real_ip: str
    _start_time: datetime.datetime
    language: str
    is_post: bool
    is_get: bool
    is_json: bool
    objdata: ObjectDict

    def __init__(self):
        raise Exception('不能实例化 只是用来代码提示')


def get_real_ip(request):
    """获取真实ip
    """
    return request.META.get('HTTP_REMOTE_ADDR2', '') or request.META.get('HTTP_X_FORWARDED_FOR',
                                                                         '') or request.META.get('REMOTE_ADDR')


class BaseMiddleware(MiddlewareMixin):
    """自定义request处理,增加一些方法和属性
    """

    def process_request(self, request):
        request.POST._mutable = True  #
        request.GET._mutable = True  # 可以使用reuqest.GET.setlist('key',[value])方法
        request.real_ip = get_real_ip(request)
        request.is_debug = DEBUG
        request._start_time = time.time()
        request.language = request.session.get('_language', '') or request.LANGUAGE_CODE or LANGUAGE_CODE
        request.language = request.language.lower()
        request.is_post = request.method == 'POST'
        request.is_get = request.method == 'GET'
        request.is_json = 'json' in request.content_type or request.path.endswith(
                '.json') or request.is_ajax() or request.GET.get('format', '') == 'json'
        # 兼容以前功能
        request.REQUEST = copy.copy(request.POST)
        request.REQUEST.update(request.GET)

    def get_check_view_func(self, request, view_func):
        view_module = sys.modules.get(view_func.__module__, None)

        if view_module:
            view_actions = getattr(view_func, 'actions', None)
            check_view_func = getattr(view_module, view_func.__name__, view_func)
            if view_actions:
                action_name = view_actions.get(request.method.lower(), '')
                if action_name:
                    check_view_func = getattr(view_func.cls, action_name, None)

            return check_view_func

    def process_view(self, request, view_func, view_args, view_kwargs):

        pass

    def process_response(self, request, response):
        return response

    def process_template_response(self, request, response):
        """
        模板渲染前,增加返回code,和msg结构
        :param request:
        :param response:
        :return:
        """

        return response

    def process_exception(self, request, exception):
        """出错处理
        """
        msg = trace_msg()
        _log.warning(msg)
        if request.is_ajax():
            rsp = RspData(code=status.HTTP_500_INTERNAL_SERVER_ERROR, msg=msg)
            return HttpResponse(json_dumps(rsp), status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                content_type='application/json')


# API 错误处理
def exception_handler(exc, context):
    """
    rest_framework api 的报错走这里
    """
    from .shortcut import RspCodeStatus
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    # elif isinstance(exc, PermissionDenied):
    #    exc = exceptions.PermissionDenied()

    # elif isinstance(exc, ValidationError):
    #   exc = exceptions.ValidationError(exc.message_dict)

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        data = None
        exc_status_msg = exc.default_detail
        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            exc_status_msg = exc.detail
        # 业务错误,http 都返回200
        status_code = status.HTTP_200_OK  # exc.status_code
        set_rollback()
        code = getattr(exc, 'code', exc.status_code)
        if isinstance(exc, ValidationError):
            code, exc_status_msg = (RspCodeStatus.ParamsError, RspCodeStatus.ParamsError.name)
        rsp = Response(data, code=code, msg=exc_status_msg, status=status_code,
                       headers=headers,
                       template_name='api_exception.html')
        return rsp
    return None
