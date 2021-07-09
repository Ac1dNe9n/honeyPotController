import pymysql
import re
import time
import os
import subprocess

# 数据库信息
host = '127.0.0.1'
user = 'root'
password = 'zx123456'
port = 3306

# 表前缀(如果没有就留空)
prefix = ''


def connectMySQL(ip, user, pwd, port):
    # 初始化数据库，开始记录日志
    connect = pymysql.connect(
        host=ip,
        user=user,
        passwd=pwd,
        port=port,
        charset='utf8'
    )
    cur = connect.cursor()
    # 开启mysql标准日志
    cur.execute('set global general_log = on')
    connect.commit()
    currentPath = 'set global log_output = \'file\''
    cur.execute(currentPath)
    connect.commit()
    # 获取连接的ip
    sql = "show variables like 'general_log_file';"
    # 执行SQL语句
    cur.execute(sql)
    # 获取所有记录列表
    results = cur.fetchall()
    logpath = results[0][1]
    connect.close()
    print(logpath)
    if not os.path.exists(logpath):
        os.remove(logpath)
        os.mknod(logpath)
    return logpath


def getIp(ip, user, pwd, port):
    # 获取连接到mysql的ip列表
    connect = pymysql.connect(
        # 开始连接数据库
        host=ip,
        user=user,
        passwd=pwd,
        port=port,
        charset='utf8'
    )
    # 获取游标
    cur = connect.cursor()
    sql = "select SUBSTRING_INDEX(host,':',1) as ip , count(*) from information_schema.processlist group by ip;"
    # 执行SQL语句
    cur.execute(sql)
    # 获取所有记录列表
    results = cur.fetchall()  # (('localhost', 4),)
    connect.close()
    iplist = []
    for ipinfo in results:
        ip = ipinfo[0]
        ipcontimes = ipinfo[1]
        iplist.append((ip, ipcontimes))
    return iplist


def monitor(logpath, host, user, password, port):
    # 监控日志新的变化
    command = 'tail -f ' + logpath
    popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    try:
        while True:
            line = popen.stdout.readline().strip()
            encodeStr = bytes.decode(line)
            pattern = re.findall('Query\s*(.*)', encodeStr, re.S)
            connect = re.findall('Connect\s*(.*)', encodeStr, re.S)
            if len(pattern) != 0:
                selectStr = pattern[0]
                if selectStr != "COMMIT":
                    joinTime = time.strftime("%H:%M:%S", time.localtime())
                    if prefix != "":
                        reg = re.findall(r'\b' + prefix + '\w*', encodeStr, re.S)
                        if len(reg) != 0:
                            table = '操作的表:' + reg[0]
                            joinTime += table
                    iplist = getIp(host, user, password, port)
                    # 只要文件变化就获取当前的连接mysql的ip
                    print((iplist, joinTime, selectStr))
                    if iplist != []:
                        print("等待传输。。。")
                        # 在这里将mysql连接的当前ip，还有时间戳和输入的指令发送给管理端
    except KeyboardInterrupt:
        os.remove(logpath)


if __name__ == '__main__':
    logpath = connectMySQL(host, user, password, port)
    time.sleep(2)
    monitor(logpath, host, user, password, port)
