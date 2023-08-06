import os, click


def ai_pkg1():
    click.echo('安装tensorflow-gpu')
    os.system('conda install -y tensorflow-gpu==1.8.0')

    click.echo('安装keras')
    os.system('conda install -y keras')

    click.echo('安装pytorch')
    os.system('conda install -y pytorch')

    click.echo('安装opencv-python')
    os.system('pip install opencv-python -i https://pypi.douban.com/simple/')
