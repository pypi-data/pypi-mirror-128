import requests
import zipfile
import os
import click


def generate_code1():
    res = requests.get('http://idea.medeming.com/jets/images/jihuoma.zip')
    with open("code.zip", "wb") as code:
        code.write(res.content)
    fz = zipfile.ZipFile("code.zip", 'r')
    for file in fz.namelist():
        filename = file.encode('cp437').decode('gbk')
        fz.extract(file)
        os.rename(file, filename)
    with open('(通用激活码)2018.2之后的版本用这个.txt', 'r') as f:
        res = f.read()
    click.echo(res)
    res = os.listdir('.')
    for item in res:
        if str(item).split('.')[-1] in ['jpg', 'txt', 'zip']:
            os.remove(item)
