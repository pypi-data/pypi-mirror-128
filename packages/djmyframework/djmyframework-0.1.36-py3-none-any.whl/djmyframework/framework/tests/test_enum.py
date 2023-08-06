from rest_framework import serializers

from ..utils.myenum import Enum,EnumElement
import pytest

@pytest.fixture(scope='session')
def django_db_setup():
    """使用现有数据库测试"""
    pass


#@pytest.mark.django_db
def test_Enum():
    def _(s):
        return s

    class EqualOperator(Enum):
        Equal = 'exact', _('等于')
        NotEqual = 'not_exact', _('等于')

    class NullOperator(Enum):
        NotNull = 'not_null', _('有值')
        IsNull = 'is_null', _('没值')

    class InOperator(Enum):
        In = 'in', _('多选')
        NotIn = 'not_in', _('反选')

    class CharOperator(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class PAGE(Enum):
        BLACK = (4, u'黑')
        WHITE = (6, u'白')

    class AD_STATUS(Enum):
        CAMPAIGN_STATUS_ENABLE = (1, u'启用')
        CAMPAIGN_STATUS_DISABLE = (2, u'暂停')

    print(type(AD_STATUS), type(AD_STATUS.CAMPAIGN_STATUS_DISABLE))

    for k, v in AD_STATUS:
        print(type(k), type(k.name))
    print(AD_STATUS, list(AD_STATUS))
    print(AD_STATUS.member_list())

    class CharOperator29(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator30(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator31(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator32(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator33(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator34(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator35(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator36(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator37(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator38(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator39(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator40(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator41(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator42(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator43(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator44(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator45(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator46(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator47(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator48(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator49(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator50(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator51(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator52(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator53(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator54(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator55(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator56(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator57(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator58(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator59(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator60(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator61(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator62(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator63(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator64(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator65(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator66(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator67(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator68(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator69(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator70(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator71(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator72(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator73(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator74(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator75(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator76(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator77(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator78(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator79(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator80(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator81(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator82(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator83(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator84(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator85(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator86(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator87(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator88(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator89(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator90(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator91(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator92(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator93(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator94(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator95(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator96(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator97(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator98(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator99(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator100(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator101(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator102(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator103(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator104(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator105(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator106(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator107(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator108(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator109(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator110(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator111(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator112(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator113(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator114(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator115(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator116(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator117(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator118(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator119(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator120(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator121(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator122(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator123(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator124(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator125(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator126(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator127(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator128(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator129(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator130(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator131(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator132(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator133(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator134(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator135(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator136(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator137(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator138(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator139(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator140(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator141(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator142(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator143(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator144(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator145(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator146(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator147(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator148(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator149(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator150(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator151(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator152(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator153(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator154(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator155(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator156(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator157(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator158(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator159(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator160(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator161(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator162(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator163(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator164(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator165(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator166(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator167(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator168(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator169(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator170(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator171(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator172(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator173(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator174(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator175(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator176(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator177(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator178(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator179(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator180(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator181(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator182(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator183(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator184(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator185(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator186(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator187(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator188(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator189(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator190(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator191(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator192(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator193(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator194(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator195(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator196(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator197(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator198(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator199(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator200(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator201(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator202(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator203(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator204(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator205(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator206(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator207(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator208(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator209(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator210(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator211(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator212(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator213(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator214(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator215(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator216(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator217(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator218(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator219(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator220(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator221(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator222(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator223(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator224(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator225(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator226(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator227(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator228(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator229(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator230(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator231(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator232(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator233(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator234(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator235(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator236(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator237(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator238(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator239(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator240(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator241(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator242(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator243(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator244(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator245(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator246(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator247(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator248(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator249(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator250(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator251(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator252(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator253(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator254(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator255(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator256(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator257(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator258(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator259(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator260(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator261(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator262(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator263(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator264(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator265(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator266(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator267(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator268(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator269(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator270(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator271(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator272(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator273(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator274(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator275(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator276(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator277(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator278(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator279(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator280(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator281(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator282(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator283(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator284(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator285(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator286(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator287(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator288(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator289(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator290(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator291(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator292(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator293(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator294(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator295(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator296(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator297(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator298(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator299(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator300(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator301(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator302(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator303(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator304(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator305(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator306(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator307(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator308(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator309(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator310(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator311(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator312(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator313(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator314(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator315(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator316(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator317(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator318(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator319(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator320(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator321(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator322(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator323(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator324(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator325(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator326(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator327(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator328(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator329(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator330(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator331(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator332(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator333(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator334(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator335(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator336(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator337(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator338(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator339(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator340(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator341(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator342(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator343(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator344(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator345(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator346(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator347(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator348(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator349(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator350(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator351(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator352(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator353(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator354(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator355(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator356(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator357(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator358(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator359(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator360(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator361(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator362(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator363(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator364(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator365(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator366(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator367(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator368(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator369(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator370(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator371(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator372(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator373(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator374(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator375(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator376(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator377(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator378(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator379(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator380(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator381(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator382(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator383(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator384(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator385(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator386(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator387(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator388(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator389(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator390(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator391(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator392(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator393(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator394(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator395(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator396(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator397(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator398(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator399(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator400(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator401(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator402(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator403(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator404(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator405(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator406(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator407(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator408(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator409(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator410(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator411(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator412(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator413(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator414(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator415(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator416(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator417(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator418(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator419(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator420(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator421(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator422(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator423(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator424(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator425(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator426(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator427(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator428(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator429(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator430(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator431(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator432(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator433(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator434(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator435(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator436(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator437(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator438(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator439(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator440(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator441(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator442(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator443(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator444(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator445(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator446(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator447(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator448(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator449(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator450(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator451(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator452(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator453(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator454(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator455(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator456(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator457(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator458(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator459(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator460(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator461(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator462(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator463(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator464(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator465(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator466(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator467(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator468(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator469(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator470(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator471(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator472(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator473(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator474(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator475(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator476(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator477(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator478(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator479(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator480(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator481(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator482(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator483(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator484(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator485(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator486(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator487(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator488(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator489(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator490(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator491(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator492(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator493(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator494(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator495(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator496(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator497(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator498(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator499(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator500(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator501(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator502(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator503(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator504(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator505(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator506(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator507(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator508(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator509(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator510(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator511(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator512(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator513(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator514(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator515(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator516(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator517(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator518(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator519(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator520(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator521(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator522(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator523(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator524(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator525(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator526(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator527(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator528(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator529(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator530(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator531(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator532(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator533(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator534(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator535(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator536(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator537(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator538(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator539(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator540(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator541(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator542(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator543(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator544(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator545(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator546(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator547(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator548(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator549(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator550(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator551(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator552(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator553(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator554(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator555(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator556(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator557(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator558(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator559(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator560(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator561(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator562(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator563(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator564(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator565(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator566(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator567(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator568(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator569(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator570(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator571(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator572(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator573(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator574(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator575(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator576(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator577(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator578(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator579(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator580(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator581(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator582(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator583(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator584(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator585(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator586(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator587(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator588(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator589(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator590(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator591(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator592(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator593(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator594(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator595(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator596(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator597(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator598(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator599(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator600(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator601(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator602(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator603(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator604(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator605(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator606(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator607(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator608(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator609(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator610(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator611(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator612(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator613(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator614(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator615(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator616(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator617(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator618(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator619(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator620(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator621(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator622(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator623(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator624(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator625(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator626(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator627(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator628(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator629(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator630(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator631(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator632(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator633(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator634(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator635(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator636(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator637(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator638(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator639(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator640(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator641(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator642(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator643(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator644(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator645(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator646(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator647(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator648(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator649(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator650(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator651(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator652(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator653(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator654(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator655(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator656(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator657(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator658(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator659(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator660(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator661(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator662(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator663(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator664(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator665(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator666(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator667(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator668(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator669(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator670(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator671(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator672(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator673(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator674(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator675(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator676(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator677(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator678(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator679(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator680(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator681(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator682(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator683(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator684(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator685(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator686(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator687(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator688(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator689(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator690(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator691(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator692(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator693(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator694(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator695(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator696(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator697(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator698(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator699(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator700(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator701(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator702(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator703(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator704(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator705(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator706(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator707(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator708(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator709(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator710(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator711(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator712(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator713(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator714(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator715(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator716(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator717(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator718(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator719(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator720(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator721(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator722(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator723(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator724(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator725(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator726(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator727(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator728(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator729(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator730(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator731(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator732(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator733(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator734(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator735(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator736(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator737(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator738(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator739(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator740(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator741(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator742(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator743(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator744(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator745(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator746(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator747(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator748(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator749(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator750(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator751(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator752(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator753(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator754(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator755(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator756(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator757(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator758(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator759(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator760(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator761(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator762(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator763(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator764(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator765(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator766(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator767(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator768(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator769(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator770(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator771(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator772(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator773(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator774(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator775(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator776(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator777(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator778(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator779(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator780(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator781(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator782(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator783(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator784(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator785(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator786(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator787(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator788(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator789(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator790(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator791(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator792(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator793(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator794(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator795(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator796(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator797(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator798(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator799(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator800(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator801(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator802(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator803(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator804(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator805(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator806(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator807(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator808(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator809(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator810(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator811(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator812(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator813(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator814(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator815(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator816(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator817(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator818(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator819(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator820(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator821(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator822(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator823(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator824(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator825(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator826(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator827(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator828(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator829(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator830(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator831(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator832(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator833(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator834(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator835(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator836(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator837(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator838(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator839(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator840(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator841(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator842(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator843(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator844(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator845(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator846(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator847(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator848(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator849(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator850(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator851(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator852(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator853(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator854(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator855(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator856(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator857(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator858(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator859(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator860(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator861(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator862(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator863(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator864(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator865(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator866(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator867(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator868(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator869(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator870(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator871(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator872(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator873(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator874(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator875(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator876(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator877(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator878(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator879(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator880(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator881(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator882(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator883(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator884(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator885(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator886(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator887(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator888(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator889(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator890(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator891(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator892(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator893(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator894(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator895(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator896(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator897(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator898(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator899(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator900(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator901(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator902(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator903(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator904(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator905(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator906(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator907(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator908(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator909(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator910(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator911(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator912(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator913(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator914(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator915(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator916(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator917(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator918(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator919(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator920(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator921(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator922(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator923(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator924(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator925(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator926(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator927(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator928(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator929(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator930(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator931(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator932(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator933(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator934(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator935(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator936(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator937(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator938(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator939(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator940(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator941(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator942(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator943(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator944(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator945(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator946(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator947(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator948(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator949(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator950(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator951(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator952(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator953(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator954(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator955(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator956(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator957(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator958(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator959(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator960(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator961(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator962(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator963(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator964(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator965(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator966(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator967(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator968(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator969(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator970(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator971(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator972(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator973(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator974(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator975(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator976(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator977(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator978(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator979(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator980(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator981(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator982(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator983(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator984(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator985(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator986(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator987(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator988(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator989(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator990(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator991(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator992(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator993(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator994(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator995(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator996(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator997(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator998(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')

    class CharOperator999(EqualOperator, NullOperator, InOperator):
        Contain = EnumElement('contains', _('包含'))
        NotContain = 'not_contains', _('不包含')
        IsEmpty = 'is_empty', _('为空')
        NotEmpty = 'not_empty', _('不为空')
        Rlike = 'rlike', _('正则匹配	匹配判断')
        NotRlike = 'not_rlike', _('正则不匹配 匹配判断')


    a= CharOperator999.Contain
    print(CharOperator999.Contain)