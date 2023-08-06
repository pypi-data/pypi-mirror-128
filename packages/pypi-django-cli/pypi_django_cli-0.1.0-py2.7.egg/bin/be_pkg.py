import os


def be_pkg1():
    os.system('pip install django==3.1 -i https://pypi.tuna.tsinghua.edu.cn/simple/')
    os.system('pip install djangorestframework==3.9.4 -i https://pypi.tuna.tsinghua.edu.cn/simple/')
    os.system('pip install django-cors-headers==3.0.2 -i https://pypi.tuna.tsinghua.edu.cn/simple/')
    os.system('pip install pymysql==0.9.3 -i https://pypi.tuna.tsinghua.edu.cn/simple/')
    os.system('pip install gunicorn==19.9.0 -i https://pypi.tuna.tsinghua.edu.cn/simple/')
    os.system('pip install django-rest-swagger==2.2.0 -i https://pypi.tuna.tsinghua.edu.cn/simple/')