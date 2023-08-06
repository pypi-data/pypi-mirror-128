import click, subprocess, json, os


def graphics_card_info(f):
    click.echo('显卡信息:')
    gpu_res = subprocess.getoutput('lspci | grep -i vga')
    if 'not found' in gpu_res:
        os.system('sudo apt-get update')
        os.system('sudo apt-get install -y pciutils')
    gpu_res = subprocess.getoutput('lspci | grep -i vga')
    click.echo(gpu_res)
    f.write('显卡:'+gpu_res+'\n')


def graphics_card_driver_info(f):
    click.echo('显卡驱动信息:')
    gpu_driver_res = subprocess.getoutput('nvidia-smi')
    if 'not found' in gpu_driver_res:
        os.system('sudo apt-get update')
        os.system('sudo apt install -y nvidia-396')
    gpu_driver_res = subprocess.getoutput('nvidia-smi')
    if 'not found' in gpu_driver_res:
        os.system('sudo apt-get update')
        os.system('sudo apt install -y nvidia-utils-390')
    gpu_driver_res = subprocess.getoutput('nvidia-smi')
    if 'not found' in gpu_driver_res:
        os.system('sudo apt-get update')
        os.system('sudo apt install -y nvidia-smi')
    gpu_driver_res = subprocess.getoutput('nvidia-smi')
    if 'failed' in gpu_driver_res or 'Failed' in gpu_driver_res:
        click.echo('显卡驱动未安装')
        f.write('显卡驱动:0\n')
    else:
        gpu_driver_res = subprocess.getoutput('nvidia-smi | grep Version')
        click.echo(gpu_driver_res)
        f.write('显卡驱动:1\n')


def anaconda_info(f):
    click.echo('Anaconda安装详情:')
    conda_res = subprocess.getoutput('conda -V')
    if 'not found' in conda_res:
        click.echo('Anaconda未安装')
        f.write('Anaconda:0\n')
    else:
        click.echo('Anaconda已安装:'+conda_res)
        f.write('Anaconda:1\n')
        conda_envs_res = subprocess.getoutput('conda info --envs')
        envs = []
        conda_envs_res = conda_envs_res.split('\n')
        for env in conda_envs_res:
            if 'envs' in env:
                envs.append(env.split(' ',maxsplit=1)[0])
        if len(envs) != 0:
            click.echo('已创建的沙盒环境有:' + json.dumps(envs))
            f.write('沙盒环境:' + json.dumps(envs) + '\n')
        else:
            click.echo('暂时未创建沙盒环境')
            f.write('未创建沙盒环境:0\n')


def docker_info(f):
    click.echo('docker安装详情:')
    docker_res = subprocess.getoutput('docker -v')
    if 'not found' in docker_res:
        click.echo('docker未安装')
        f.write('docker:0\n')
    else:
        click.echo('docker已安装:'+docker_res)
        f.write('docker:1\n')


def nvidia_docker_info(f):
    click.echo('nvidia-docker安装详情:')
    nvidia_docker_res = subprocess.getoutput('nvidia-docker -v')
    if 'not found' in nvidia_docker_res:
        click.echo('nvidia-Docker未安装')
        f.write('nvidia-Docker:0\n')
    else:
        nvidia_docker_res = subprocess.getoutput('sudo nvidia-docker version')
        click.echo('nvidia-Docker已安装\n'+nvidia_docker_res)
        f.write('nvidia-Docker:1\n')


def ai_check1():
    f = open('status.txt', 'w')
    f.write('该文件表明环境安装情况：状态0表示未安装，状态1表示已安装\n')
    graphics_card_info(f)
    graphics_card_driver_info(f)
    anaconda_info(f)
    docker_info(f)
    nvidia_docker_info(f)
    f.close()