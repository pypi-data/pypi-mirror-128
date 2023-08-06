# -*- coding: utf-8 -*-
# @Time    : 2021/11/2 11:34 
# @Author  : xzr
# @File    : urls.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :


from django.urls import path as _path


def get_view_name(view_module):
    return '%s.%s' % (view_module.__module__, view_module.__name__)


def path(route, view, kwargs=None, name=None):
    if not name:
        name = get_view_name(view)
    return _path(route, view, kwargs=kwargs, name=name)
