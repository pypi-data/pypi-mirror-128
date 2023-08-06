from framework.response import JsonResponse, RspError, RspErrorEnum
from framework.utils.myenum import Enum
from framework.translation import _
from framework.views import CurdViewSet, api_post, api_get, api_doc
from framework.route import Route


class RspCodeStatus(Enum):
    """系统常用返回状态"""

    Success = 0, _('成功')
    Fail = 1, _('失败,查看具体消息')
    NotLoggedIn = -1, _('权限不足，请先登录')
    NotPermission = -2, _('权限不足')
    ParamsError = -4, _('参数格式错误')
    DuplicatePay = 99, _('给闸机重复支付限制使用')


def Response(code=0, msg='', data=None):
    """
    把常用的返回弄一个快捷方式
    """
    status_code = RspCodeStatus(code)
    if status_code is not None:
        msg = msg or RspCodeStatus(code).name
    return JsonResponse(code=code, msg=msg, data=data).render()


class APIError(Exception):
    def __init__(self, msg=None, code=1, data=None):
        self.msg = msg
        self.code = code
        self.data = data

    def __str__(self):
        return str(self.msg)

    def as_response(self):
        return Response(self.code, self.msg, self.data)


class CommonError(Exception):
    def __init__(self, msg=None, code=None):
        self.msg = msg
        self.code = code

    def __str__(self):
        return str(self.msg)

    def as_response(self):
        return Response(self.code, self.msg)
