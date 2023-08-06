# -*- coding: utf-8 -*-
"""
check the request.POST or request.GET whether vaild
"""

from django.http import QueryDict


class RequestError(Exception):
    def __init__(self, msg):
        super(RequestError, self).__init__()
        self.msg = msg

    def __str__(self):
        return self.msg


def must_be_int(query_dict: QueryDict, *args):
    for key in args:
        value = query_dict.get(key)
        try:
            int(value)
        except (TypeError, ValueError):
            raise RequestError('{}必须为整数'.format(key))


def can_not_none(query_dict: QueryDict, *args):
    for key in args:
        value = query_dict.get(key)
        if value is None:
            raise RequestError('{}必须存在'.format(key))


def can_not_empty(query_dict: QueryDict, *args):
    for key in args:
        value = query_dict.get(key)
        if isinstance(value, str) and value.strip() == '':
            raise RequestError('{}不能为空'.format(key))
