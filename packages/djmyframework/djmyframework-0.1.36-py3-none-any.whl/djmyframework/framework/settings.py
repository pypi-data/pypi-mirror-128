
from __future__ import absolute_import
from django.conf import settings
import sys
import os
import jinja2

############ REST_FRAMEWORK设置 ########
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        # 'framework.renderers.DebugRenderer',
        # 这里顺序不要更换
        'rest_framework.renderers.TemplateHTMLRenderer',
        'framework.renderers.JSONRenderer',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'EXCEPTION_HANDLER': 'framework.middleware.exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': ('framework.authentication.MySessionAuthentication',)
}
DRF_DYNAMIC_FIELDS = {'SUPPRESS_CONTEXT_WARNING': True}

#######################################


############# 数据库连接池 配置 #############
DJORM_POOL_OPTIONS = {
    "pool_size": 5,
    "max_overflow": 0,
    "recycle": 3600,  # the default value
}
########################################

# session引擎设置
# SESSION_ENGINE='django.contrib.sessions.backends.cache'
# SESSION_COOKIE_AGE = 60 * 30  # 30分钟
# SESSION_SAVE_EVERY_REQUEST = True
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 关闭浏览器，则COOKIE失效


############# api 文档设置 ##############
SWAGGER_SETTINGS = {
    # https://drf-yasg.readthedocs.io/en/stable/security.html
    'USE_SESSION_AUTH': True,
   # 'DEFAULT_INFO'             : 'config.api_doc.API_INFO',
    'DEFAULT_AUTO_SCHEMA_CLASS': 'framework.schema.CustomSwaggerAutoSchema',
}
########################################

X_FRAME_OPTIONS = 'SAMEORIGIN'

TEMPLATE_DIR = os.path.join(settings.BASE_DIR, 'jinja2_templates')

TEMPLATES = [
    {
        'BACKEND': 'framework.jinja2_env.TemplateJinja2Backend',
        'DIRS': [os.path.join(settings.BASE_DIR, 'jinja2_templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'framework.context_processors.context_settings'
            ],
            'environment': 'framework.jinja2_env.environment',
            'undefined': jinja2.Undefined
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]




# 密码加密策略,使用
PASSWORD_HASHERS = [
    'framework.authentication.LDAPSHA1PasswordHasher',
]

VIEWS_DIR = 'controller'
ROUTE_PREFIX = ''
ROUTE_APP_PREFIX_MAP = {}
APPS_ROOT = 'apps'