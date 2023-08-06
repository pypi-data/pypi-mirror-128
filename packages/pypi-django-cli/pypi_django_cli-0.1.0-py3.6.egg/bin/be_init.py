import os
from django.utils.crypto import get_random_string


def get_random_secret_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return get_random_string(50, chars)
key = get_random_secret_key()


def init_project(n,e):
    os.mkdir(n)
    os.mkdir(n+'/'+n)
    with open(n+'/'+n+'/__init__.py', 'w') as f:
        f.write('')
    with open(n+'/'+n+'/urls.py', 'w') as f:
        f.write('''from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
]
        ''')
    with open(n+'/'+n+'/wsgi.py', 'w') as f:
        f.write('''import os     

from django.core.wsgi import get_wsgi_application

env = os.environ.get("ENV")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.%%s" %% env)

application = get_wsgi_application()
        '''%n)
    with open(n+'/'+n+'/settings.py', 'w') as f:
        f.write('''import os
import json

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_address = os.path.join(BASE_DIR, 'secrets.json')
with open(file_address) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_secret("SECRET_KEY")


DEBUG = True

ALLOWED_HOSTS = ['*']



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '%s.urls'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['rest_framework.filters.OrderingFilter', ]
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = '%s.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "%s",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^.*$'

Access_Control_Allow_Origin='*'
        '''%(n,n,n))
    with open(n+'/'+n+'/dev.py', 'w') as f:
        f.write('''from %s.settings import *

SETTINGS_ENV = 'dev'

DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES['default']['USER'] = get_secret("DATABASE_USER_DEV")
DATABASES['default']['PASSWORD'] = get_secret("DATABASE_PASSWORD_DEV")
DATABASES['default']['HOST'] = get_secret("DATABASE_HOST_DEV")
DATABASES['default']['PORT'] = get_secret("DATABASE_PORT_DEV")
        '''%(n))
    with open(n+'/'+n+'/beta.py', 'w') as f:
        f.write('''from %s.settings import *

SETTINGS_ENV = 'beta'

DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES['default']['USER'] = get_secret("DATABASE_USER_BETA")
DATABASES['default']['PASSWORD'] = get_secret("DATABASE_PASSWORD_BETA")
DATABASES['default']['HOST'] = get_secret("DATABASE_HOST_BETA")
DATABASES['default']['PORT'] = get_secret("DATABASE_PORT_BETA")
        ''' % (n))
    with open(n+'/'+n+'/production.py', 'w') as f:
        f.write('''from %s.settings import *

SETTINGS_ENV = 'production'

DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES['default']['USER'] = get_secret("DATABASE_USER_PRODUCTION")
DATABASES['default']['PASSWORD'] = get_secret("DATABASE_PASSWORD_PRODUCTION")
DATABASES['default']['HOST'] = get_secret("DATABASE_HOST_PRODUCTION")
DATABASES['default']['PORT'] = get_secret("DATABASE_PORT_RODUCTION")
        '''%(n))


def init_files(n,e):
    with open(n + '/.gitignore', 'w') as f:
        f.write('''.idea/
logs/
*.pot
*.py[co]
.tox/
__pycache__
MANIFEST
dist/
docs/_build/
docs/locale/
node_modules/
tests/coverage_html/
tests/.coverage
tests/report/
.DS_Store
*.swp
.code/
        ''')
    with open(n+'/secrets.json', 'w') as f:
        f.write('''{
  "SECRET_KEY": "%s",
        
  "DATABASE_HOST_DEV": "pg.test.smartahc.com",
  "DATABASE_USER_DEV": "postgres",
  "DATABASE_PASSWORD_DEV": "smart123",
  "DATABASE_PORT_DEV":"5432",
  
  "DATABASE_HOST_BETA":"",
  "DATABASE_USER_BETA": "",
  "DATABASE_PASSWORD_BETA":"",
  "DATABASE_PORT_BETA":"",

  "DATABASE_HOST_PRODUCTION":"",
  "DATABASE_USER_PRODUCTION": "",
  "DATABASE_PASSWORD_PRODUCTION":"",
  "DATABASE_PORT_PRODUCTION":""
}
        '''%key)
    with open(n+'/requirements.txt', 'w') as f:
        f.write('''django==2.1
djangorestframework==3.9.4
django-cors-headers==3.0.2
pymysql==0.9.3
gunicorn==19.9.0
psycopg2-binary
django-mptt==0.9.0
djangorestframework-expiring-authtoken
oss2
djangorestframework-bulk==0.2.1
        ''')
    with open(n+'/manage.py', 'w') as f:
        f.write('''#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.%s')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
        '''%(n, e))
    with open(n+'/gunicorn.conf', 'w') as f:
        f.write('''workers = 3
bind = '0.0.0.0:80'
        ''')
    with open(n+'/entrypoint.sh', 'w') as f:
        f.write('''#!/bin/bash

gunicorn -c gunicorn.conf %s.wsgi:application
        '''%n)
    with open(n+'/Dockerfile', 'w') as f:
        f.write('''FROM python:3.6-slim

COPY ./requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /app/

EXPOSE 80

ENTRYPOINT [ "bash","./entrypoint.sh" ]
        ''')
    with open(n+'/README.md','w') as f:
        f.write('''## 环境依赖
- django==2.1
- djangorestframework==3.9.4
- django-cors-headers==3.0.2
- pymysql==0.9.3
- gunicorn==19.9.0
- psycopg2-binary
- django-mptt==0.9.0
- djangorestframework-expiring-authtoken
- oss2
- djangorestframework-bulk==0.2.1

## 目录介绍
```
 ├── %s                            //项目文件夹
 │    |--__init__.py
 |    |--urls.py
 |    |--wsgi.py
 |    |--settings.py
 |    |--base.py
 |    |--dev.py
 |    |--production.py
 │
 ├── code.json                      //错误码
 │
 ├── Dockerfile                     //Dockerfile
 │
 ├── enterypoint.sh                 //项目启动脚本
 │  
 ├── gunicorn.conf                  //gunicorn配置文件
 │                  
 ├── manage.py                      //manage.py
 │                  
 ├── README.md                      //README.md
 │                 
 ├── requirements.txt               //三方库   
 │ 
 └── secrets.json                   //数据库配置
```

## 项目运行
- 首先在secrets.json文件中配置数据库连接信息
- 本地运行,首先迁移数据库生成表,然后运行,迁移和运行时可以指定环境为local,test_server,production
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver --settings=settings.local
```
- 打包运行,首先构建docker镜像，运行镜像的时候指定好运行环境,环境为local,test_server,production其中一种,命令如下
```
sudo docker build -t test:v1 .
sudo docker run -it -e ENV=local -p 8000:80 test:v1
```
        '''%n)


def init_utils(n):
    os.mkdir(n+'/utils')
    with open(n+'/utils/pagination_tools.py', 'w') as f:
        f.write('''from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.core.paginator import InvalidPage
from django.utils import six


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100000

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        Update self.page_size, if page_size_query_param appears in the request url
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None
        else:
            self.page_size = page_size

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=six.text_type(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('page_size', self.page_size),
            ('current_page', self.page.number),
            ('last_page', self.page.paginator.num_pages),
            ('count', self.page.paginator.count),
            ('data', data)
        ]))
        ''')
    with open(n+'/utils/search_tools.py', 'w') as f:
        f.write('''def is_search_param(item):
    """
    Filter search params
    """
    if item[0].startswith("search_"):
        return True
    return False


def get_search_param(item):
    return (item[0][7:], item[1])


def search_decorator(f):
    """
    decorate get_queryset method
    do further filtering
    URL carries param: search_QUERY
    QUERY is a string follows query rule of Django model
    """
    def wrapper(*args, **kwargs):
        queryset = f(*args, **kwargs)

        items = args[0].request.query_params.items()
        items = filter(is_search_param, items)
        search_items = map(get_search_param, items)
        search_dict = {key: value for key, value in search_items}

        try:
            if len(search_dict) > 0:
                queryset = queryset.filter(**search_dict)
        except Exception as e:
            print(e)
        return queryset

    return wrapper
        ''')


def be_init1(n,e):
    #初始化项目目录
    init_project(n,e)
    #初始化配置文件
    init_files(n,e)
    #初始化工具函数
    init_utils(n)