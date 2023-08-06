# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @Time: ${datetime}

from framework.translation import _
from framework.serializer import s, BaseModelSerializer, EditParams, IdSerializer, IdsSerializer, ParamsSerializer, \
    ParamsPaginationSerializer, PaginationSerializer, ModelFilterSerializer, ListIntField, ListStrField
from ${app_name}.models import ${model_name}


class ${model_name}Serializer(BaseModelSerializer):
    # https://www.django-rest-framework.org/api-guide/serializers/
    # https://www.django-rest-framework.org/api-guide/relations/
% for f in model_many_to_many:
    #${f.name} = s.PrimaryKeyRelatedField(many=True, label=_("${f.verbose_name}"), queryset=${model_name}.${f.name}.field.related_model.objects.all() )
% endfor
% for f in model_foreigns:
    #${f.name} = s.RelatedField(label=_("${f.verbose_name}"), queryset=${model_name}.${f.name}.field.related_model.objects.all())
% endfor
% for f in fields:
    % if f.choices:
    ${f.name}_alias = s.CharField(source='get_${f.name}_display', required=False, read_only=True)
    % endif
% endfor

    class Meta:
        model = ${model_name}
        fields = ${all_fields_name_list} or '__all__'
        #exclude = ['session_key']
        read_only_fields = ['create_time', 'update_time']
        #extra_kwargs = {'password': {'write_only': True}}

class List${model_name}ReqSerializer(ModelFilterSerializer, ParamsPaginationSerializer):
    model_class = ${model_name}
    filter_fields = ${list(fields_name_list)}


class List${model_name}RspSerializer(PaginationSerializer):
    results = ${model_name}Serializer(many=True, required=False)
