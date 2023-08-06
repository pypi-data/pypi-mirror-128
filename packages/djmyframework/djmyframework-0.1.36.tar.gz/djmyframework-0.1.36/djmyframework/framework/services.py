# -*- coding: utf-8 -*-
# @Time    : 2021/10/21 10:51 
# @Author  : xzr
# @File    : service.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :


from django.db import models
from django.core.paginator import Paginator
from django.db.models import Q


class BaseService(object):
    """模型 服务"""
    model: models.Model = None

    queryset: models.QuerySet = None

    def get_queryset(self) -> models.QuerySet:
        """获取查询"""
        raise Exception('重写 get_queryset 方法!')

    def list(self, *args, **kwargs):
        """查询列表"""

    def list(self, filter_params, page_num=1, page_size=100):
        """查询 模型 列表"""

        queryset = self.get_queryset()
        queryset = queryset.filter(filter_params) if isinstance(filter_params, Q) else queryset.filter(
                **filter_params)
        pagination = Paginator(queryset, page_size)
        num_pages = pagination.num_pages
        page_contents = pagination.page(page_num)
        count = pagination.count
        return count, num_pages, page_contents

    def save(self, *args, **kwargs):
        """保存实例"""
        pass
