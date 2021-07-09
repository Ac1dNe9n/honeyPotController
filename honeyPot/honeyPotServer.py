import docker

docker_client = docker.from_env()


def addWebDocker(id, port):
    try:
        docker_client.containers.run(
            'webcanary',
            stdin_open=True,
            tty=True,
            detach=True,
            privileged=True,
            ports={
                '8000/tcp': port
            },
            hostname='Web' + id,
            name='Web' + id,
        )
    except:
        print("error")


def restartWebDockear(id):
    try:
        container = docker_client.containers.get('Web' + id)
        port = container.attrs['NetworkSettings']['Ports']['8000/tcp'][0]['HostPort']
        delWebDocker(id)
        addWebDocker(id, port)
    except:
        print("error")


def delWebDocker(id):
    try:
        container = docker_client.containers.get('Web' + id)
        if container == "":
            return
        if container.status == 'running':
            container.stop()
        container.remove()
    except:
        print("error")


def addMysqlDocker(id, port):
    try:
        docker_client.containers.run(
            'mysqlcanary',
            stdin_open=True,
            tty=True,
            detach=True,
            privileged=True,
            ports={
                '3306/tcp': port
            },
            hostname='Mysql' + id,
            name='Mysql' + id,
        )
    except:
        print("error")


def restartMysqlDockear(id):
    try:
        container = docker_client.containers.get('Mysql' + id)
        port = container.attrs['NetworkSettings']['Ports']['3306/tcp'][0]['HostPort']
        delMysqlDocker(id)
        addMysqlDocker(id, port)
    except:
        print("error")


def delMysqlDocker(id):
    try:
        container = docker_client.containers.get('Mysql' + id)
        if container.status == 'running':
            container.stop()
        container.remove()
    except:
        print("error")
