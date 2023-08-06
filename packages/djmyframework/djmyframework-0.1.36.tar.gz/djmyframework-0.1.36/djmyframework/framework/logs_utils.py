# -*- coding: utf-8 -*-
import json
import socket
import traceback

from django.conf import settings
from requests_futures.sessions import FuturesSession


def send_logs(request, response, debug_info=None, exception_html=None):
    try:
        # 计算请求头部
        request_headers = {'-'.join([i.capitalize() for i in k.split('_')][1:]): request.META[k]
                           for k in request.META if k.startswith('HTTP_')}
        request_headers.update({'Content-Type': request.META.get('CONTENT_TYPE', '')})

        # 计算请求体内容
        if request.method == 'POST':
            if ('multipart/form-data' in request_headers['Content-Type'] or
                    '' in request_headers['Content-Type']):
                request_body = {k: request.POST[k] for k in request.POST}
                if 'multipart/form-data' in request_headers['Content-Type']:
                    for i in request.FILES:
                        request_body[i] = {
                            'size': request.FILES[i].size,
                            'content_type': request.FILES[i].content_type,
                            'name': request.FILES[i].name}
                request_body = json.dumps(request_body)
            else:
                request_body = str(request.body.read())
        else:
            request_body = ''
        request_headers = json.dumps(request_headers)

        # 计算GET参数列表
        url_params = json.dumps({i: request.GET[i] for i in request.GET})

        # 计算response_body
        response_body = ''
        if response.status_code == 500:
            response_body = exception_html
        else:
            if hasattr(response, 'content'):
                if type(response.content) == bytes:
                    response_body = response.content.decode('utf-8')
                else:
                    response_body = str(response.content)

        # 计算client_info和server_info
        client_info = json.dumps({'client_ip': request.ip})
        server_info = json.dumps({'hostname': socket.gethostname()})

        # 计算extra_info
        extra_info = {}
        if debug_info:
            extra_info['debug_info'] = debug_info
        try:
            extra_info = json.dumps(extra_info)
        except:
            extra_info = json.dumps({})

        data = {
            'project_name': settings.PROJECT_NAME,
            'url': request.path,
            'url_params': url_params,
            'request_header': request_headers,
            'request_body': request_body,
            'status_code': response.status_code,
            'response_body': response_body,
            'client_info': client_info,
            'server_info': server_info,
            'extra_info': extra_info,
        }

        url = 'https://internal-service.packertec.com/api/logs/api_log/add'
        # 验证头部
        service_auth_header = {
            'Internal-Secret-Key': settings.PACKER_SERVICE['internal-service']['Internal-Secret-Key']}

        # 异步发送
        FuturesSession().post(url, data=data, headers=service_auth_header)
    except Exception as e:
        traceback.print_exc()
