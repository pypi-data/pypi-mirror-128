# -*- coding: utf-8 -*-
# @Time    : 2021/10/20 10:16 
# @Author  : xzr
# @File    : request.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :


from rest_framework.request import Request as RestRequest
from rest_framework.request import Empty
from .utils.cache import CacheAttribute
from objectdict import ObjectDict


class MyRequest(RestRequest):

    # @CacheAttribute
    # def data(self):
    #     self._full_data = ObjectDict(super().data)
    #     self._full_data.update(dict(self.query_params.items()))
    #     return self._full_data

    @property
    def POST(self):
        # Ensure that request.POST uses our request parsing.
        if self._data is Empty:
            self._load_data_and_files()
        return self._data

    def force_plaintext_errors(self, value):
        """取消 ajax 返回 html"""
        pass


Request = MyRequest
