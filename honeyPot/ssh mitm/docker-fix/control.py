from typing import Tuple
import docker
from datetime import datetime

from ctlcmd import *



docker_client = docker.from_env()
mitm_name = 'mitm_test'
volume_path = '/home/zimarnt/work/docker/ip2key'
log_path = '/home/zimarnt/work/docker/mitm_log'


def cmdPack(cmd: str):
    cmd_pattern = "bash -c '{bash_script}'"
    cmd_pack = {'bash_script': cmd}
    return cmd_pattern.format(**cmd_pack)

def checkStatus(name: str):
    container = docker_client.containers.get(name)
    return container.status


def containersList(all=False):
    containers_list = []
    ip_list = []
    for container in docker_client.containers.list(
            all=False,
            filters={
                'ancestor': 'victim',
            }):
        containers_list += [container.name]
        ip_list += [container.attrs['NetworkSettings']['Networks']['bridge']['IPAddress']]
    for container in docker_client.containers.list(
            all=False,
            filters={
                'ancestor': 'forward',
            }):
        containers_list += [container.name]
        ip_list += [container.attrs['NetworkSettings']['Networks']['bridge']['IPAddress']]
    if all == True:
        # 把监听机也列入队列
        # 所以平常只是返回所有靶机的id
        for container in docker_client.containers.list(
                all=False,
                filters={
                    'ancestor': 'mitm',
                }):
            containers_list += [container.name]
            ip_list += [container.attrs['NetworkSettings']['Networks']['bridge']['IPAddress']]
    return containers_list, ip_list

def createVictim(name=None):
    # 一定要在build的时候固定好image名字
    if name == None:
        name = datetime.now().strftime("%y-%m-%dT%H.%M.%S")
    container = docker_client.containers.run(
        'victim',
        stdin_open=True,
        tty=True,
        detach=True,
        privileged=True,
        volumes={
            volume_path: {
                'bind': '/work/ip2key',
                'mode': 'rw',
            }
        },
        hostname=name,
        name=name,
    )
    # DEBUG
    # r = container.exec_run(cmdPack(test_cmd))
    r = container.exec_run(cmdPack(create_cmd))
    print(r)

    port = assignPort(name)

    mitm_ips = ';'.join(containersList(all=False)[1])
    createMitm(mitm_ips)
    return name, port


def destoryVictim(name: str):
    container = docker_client.containers.get(name)
    if container.status == 'running':
        sleepVictim(name)
    # 在暂停容器时就已经完成了收尾工作
    # 由于已经暂停了，所以也不能执行收尾指令
    # 故而，注释
    # r = container.exec_run(cmdPack(destory_cmd))
    # print(r)
    container.remove()

    # 删除转发节点
    forward_container = docker_client.containers.get('Forward.'+name)
    forward_container.stop()
    forward_container.remove()

    mitm_ips = ';'.join(containersList(all=False)[1])
    createMitm(mitm_ips)


def sleepVictim(name: str):
    container = docker_client.containers.get(name)
    # DEBUG
    # r = container.exec_run(cmdPack(test_cmd))
    r = container.exec_run(cmdPack(sleep_cmd))
    print(r)
    container.stop()

    mitm_ips = ';'.join(containersList(all=False)[1])
    createMitm(mitm_ips)


def weakupVictim(name: str):
    container = docker_client.containers.get(name)
    container.restart()
    # DEBUG
    # r = container.exec_run(cmdPack(test_cmd))
    r = container.exec_run(cmdPack(weakup_cmd))
    print(r)

    mitm_ips = ';'.join(containersList(all=False)[1])
    createMitm(mitm_ips)


def createMitm(mitm_ips):
    try:
        container = docker_client.containers.get(mitm_name)
    except docker.errors.NotFound:
        pass
    else:
        container.stop()
        container.remove()
    container = docker_client.containers.run(
        'mitm',
        stdin_open=True,
        tty=True,
        detach=True,
        privileged=True,
        environment=[f'MITMIPS={mitm_ips}'],
        volumes={
            volume_path: {
                'bind': '/work/ip2key',
                'mode': 'rw',
            },
        },
        #ports={
        #    '8081/tcp': 8081
        #},
        hostname=mitm_name,
        name=mitm_name,
    )
    # DEBUG
    # r = container.exec_run(cmdPack(test_cmd))
    r = container.exec_run(cmdPack(start_listening_cmd))

    print(r)

def destoryMitm():
    container = docker_client.containers.get(mitm_name)
    if container.status == 'running':
        container.stop()
    container.remove()

def assignPort(name:str):
    try:
        container = docker_client.containers.get('Forward.'+name)
    except docker.errors.NotFound:
        pass
    else:
        container.stop()
        container.remove()

    container = docker_client.containers.run(
        'forward',
        stdin_open=True,
        tty=True,
        detach=True,
        privileged=True,
        ports={
            '22/tcp': None # 随机分配一个
        },
        hostname='Forward.'+name,
        name='Forward.'+name,
    )
    to_container = docker_client.containers.get(name)
    to_ipaddr = to_container.attrs['NetworkSettings']['Networks']['bridge']['IPAddress']
    # DEBUG
    # r = container.exec_run(cmdPack(test_cmd))
    to_ipaddr_pack = {'to_ipaddr': to_ipaddr}
    r = container.exec_run(cmdPack(forward_cmd.format(**to_ipaddr_pack)))
    print(r)

    container = docker_client.containers.get('Forward.'+name)
    port = container.attrs['NetworkSettings']['Ports']['22/tcp'][0]['HostPort']
    return port

def recoverVictim(name: str):
    destoryVictim(name)
    name, port = createVictim(name)
    return name, port

def createPlayGround(name=None):
    if name == None:
        name = datetime.now().strftime("PlayGround.%y-%m-%dT%H.%M.%S")
    container = docker_client.containers.run(
        'sqli-labs',
        stdin_open=True,
        tty=True,
        detach=True,
        privileged=True,
        ports={
            '80/tcp': None # 随机分配一个
        },
        hostname=name,
        name=name,
    )

def destoryPlayGround(name:str):
    container = docker_client.containers.get(name)
    if container.status == 'running':
        container.stop()
    container.remove()

def recoverPlayGround(name: str):
    destoryPlayGround(name)
    createPlayGround(name)

if __name__ == '__main__':
    # createPlayGround()
    # recoverPlayGround('PlayGround.21-07-08T20.55.34')
    # destoryPlayGround('PlayGround.21-07-08T20.57.48')
    createVictim('ssh1')
    createVictim('ssh2')
    # createVictim()
    # sleepVictim('21-07-08T02.03.28')
    # weakupVictim('21-07-08T02.03.28')
    # destoryVictim('ssh')
    # recoverVictim('21-07-08T17.21.36')
    # destoryMitm()
    # mitm_ips = ';'.join(containersList(all=False)[1])
    # createMitm(mitm_ips)
    # mitmStartListening()
    # mitmStopListening()

    print(containersList(all=False))
