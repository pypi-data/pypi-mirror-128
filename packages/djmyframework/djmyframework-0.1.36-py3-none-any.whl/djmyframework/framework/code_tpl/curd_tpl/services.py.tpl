# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @Time: ${datetime}


from framework.translation import _
from ${app_name}.models import ${model_name}
from django.db import transaction
from framework.services import BaseService
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum, When, Case
<%!
from django.db.models.fields import IntegerField,CharField,DateTimeField,BigAutoField,TextField,NOT_PROVIDED,BooleanField,FloatField,EmailField
from django.db.models.fields.related import ManyToManyField,ForeignKey,OneToOneField
from framework.models import BaseModelMixin
%>
class ${model_name}Service(BaseService):
    """${app_verbose_name} ${model_desc} 服务"""

    model = ${model_name}

    def list(self, filter_params, page_num=1, page_size=100, filter_q=None):
        """${model_desc} 列表"""

        queryset = ${model_name}.objects.all().prefetch_related(*${[f.name for f in model_many_to_many]}).select_related(*${[f.name for f in model_foreigns]})
        queryset = queryset.filter(**filter_params)
        pagination = Paginator(queryset, page_size)
        num_pages = pagination.num_pages
        page_contents = pagination.page(page_num)
        count = pagination.count
        return count, num_pages, page_contents

    def save(self, params_data):
        """${model_desc} 保存"""
        with transaction.atomic():
            if params_data.id:
                ${model_lower_name} = ${model_name}.objects.filter(id=params_data.id).first()
            else:
                ${model_lower_name} = ${model_name}()

            % for f in fields:

            % if isinstance(f,ManyToManyField):
            ${model_lower_name}.${f.name}.add(params_data.${f.name})
            % elif isinstance(f,(ForeignKey,OneToOneField)):
            ${model_lower_name}.${f.name} = params_data.${f.name}
            % elif f.name!='id':
            ${model_lower_name}.${f.name} = params_data.${f.name}
            % endif
            % endfor
            ${model_lower_name}.save()
        return ${model_lower_name}


