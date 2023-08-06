# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @Time: ${datetime}


from framework.filters import MyFilterBackend, OrderingFilter, MyFilterSerializer
from framework.translation import _
from framework.route import Route
from framework.serializer import s,BaseModelSerializer, EditParams, IdSerializer, IdsSerializer, ParamsSerializer,ParamsPaginationSerializer,PaginationSerializer,ModelFilterSerializer
from framework.views import CurdViewSet, ListPageNumberPagination,action,api_doc
from framework.views import render_to_response as rt
from ${app_name}.models import ${model_name}
from django.db import transaction
from django.db.models import Q, Count, Sum, When, Case
from collections import OrderedDict
from framework.shortcut import APIError,Response,api_doc,api_get,api_post
from ${app_name}.services.${model_lower_name} import ${model_name}Service
from framework.serializer import CeleryTaskResultSerializer
from ${app_name}.serializer.${model_lower_name} import *
from middlewares import EnhanceRequest


@Route('${app_name}/${model_lower_name}')
class ${model_name}Set(CurdViewSet):
    """${app_verbose_name}${model_desc}"""

    request: EnhanceRequest

    serializer_class = ${model_name}Serializer

    # 可条件过滤的字段
    filter_fields = List${model_name}ReqSerializer.filter_fields

    # 可以查询字段
    queryset_fields = ${list(fields_name_list)}

    model = ${model_name}

    def get_queryset(self):
        return ${model_name}.objects.all().prefetch_related(*${[f.name for f in model_many_to_many]}).select_related(*${[f.name for f in model_foreigns]}).only(*${model_name}Set.queryset_fields)

    def get_filter_params(self,params_data=None):
        filter_params = {}
        filter_params.update(MyFilterBackend().get_filter_dict(self.request.REQUEST, self.filter_fields))
        return filter_params

    @api_doc(tags=['${app_verbose_name}'], request_body=List${model_name}ReqSerializer, responses=List${model_name}RspSerializer)
    def list(self, request:EnhanceRequest,is_export=False):
        """${model_desc}列表 ${app_name}.${model_lower_name}.list"""

        params_data = List${model_name}ReqSerializer(request.data).params_data
        filter_params = self.get_filter_params(params_data)

        if is_export:
            pass
            #from ..tasks import ${model_lower_name}_list_export
            #result = ${model_lower_name}_list_export.delay(filter_params)
            #return Response(data=dict(query_id=result.id))

        total_count, num_pages, page_contents = ${model_name}Service().list(filter_params,params_data.page,params_data.page_size)

        serializer = ${model_name}Serializer(page_contents, many=True)
        data = OrderedDict(
                count=total_count,
                page=params_data.page,
                page_size=params_data.page_size,
                results=serializer.data,
                filter=params_data
        )
        return Response(data=data)


    @api_doc(tags=['${app_verbose_name}'], request_body=List${model_name}ReqSerializer, responses=List${model_name}RspSerializer)
    @api_post
    def list_export(self, request:EnhanceRequest):
        """${model_desc}列表导出 ${app_name}.${model_lower_name}.list_export"""
        return self.list(request,is_export=True)



    @api_doc(tags=['${app_verbose_name}'], request_body=${model_name}Serializer, responses=${model_name}Serializer)
    def add(self, request:EnhanceRequest):
        """${model_desc}新增 ${app_name}.${model_lower_name}.add"""

        params_data = ${model_name}Serializer(request.data).params_data
        params_data.id = 0
        ${model_lower_name} = ${model_name}Service().save(params_data)
        data = ${model_name}Serializer(instance=${model_lower_name})

        return Response(data=data)


    @api_doc(tags=['${app_verbose_name}'], request_body=${model_name}Serializer, responses=${model_name}Serializer)
    def modify(self, request:EnhanceRequest):
        """${model_desc}更改 ${app_name}.${model_lower_name}.modify"""

        params_data = ${model_name}Serializer(request.data).params_data
          if not params_data.id:
            raise APIError(_('未指定ID'))
        ${model_lower_name} = ${model_name}Service().save(params_data)
        data = ${model_name}Serializer(instance=${model_lower_name})
        return Response(data=data)


    @api_doc(tags=['${app_verbose_name}'], request_body=IdsSerializer, responses=IdsSerializer)
    def delete(self, request:EnhanceRequest):
        """${model_desc}删除 ${app_name}.${model_lower_name}.delete"""
        params_data = IdsSerializer(request.data).params_data
        if params_data.ids:
            self.get_queryset().filter(id__in=params_data.ids).delete()

        return Response(data=params_data)



