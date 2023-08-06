import os, click


def install_anaconda(text):
    for i in text:
        if 'Anaconda:0' in i:
            os.system('sudo apt-get -y update')
            os.system('sudo apt-get -y install wget')
            os.system('sudo wget http://repo.anaconda.com/archive/Anaconda3-5.0.0.1-Linux-x86_64.sh')
            os.system('bash Anaconda3-5.0.0.1-Linux-x86_64.sh')


def install_docker(text):
    for i in text:
        if 'docker:0' in i:
            os.system('sudo apt-get -y update')
            os.system('sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common')
            os.system('curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -')
            os.system('sudo add-apt-repository "deb [arch=amd64] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"')
            os.system('sudo apt-get -y update')
            os.system('sudo apt-get -y install docker-ce')


def install_nvidia_docker(text):
    for i in text:
        if 'nvidia-Docker:0' in i:
            os.system('curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -')
            os.system('distribution=$(. /etc/os-release;echo $ID$VERSION_ID);curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list')
            os.system('sudo apt-get -y update')
            os.system('sudo apt-get install -y nvidia-docker')
            os.system('sudo pkill -SIGHUP dockerd')


def ai_env1():
    f = open('status.txt','r')
    text = f.readlines()
    click.echo('安装anaconda')
    install_anaconda(text)
    click.echo('安装docker')
    install_docker(text)
    click.echo('安装nvidia-docker')
    install_nvidia_docker(text)
    f.close()
