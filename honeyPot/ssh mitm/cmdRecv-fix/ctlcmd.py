get_ip = '''
host_ip=`hostname -I`
host_ip=${host_ip:0:-1}
ip2key_path='/work/ip2key'
'''

create_cmd = f'''
{get_ip}
DEBIAN_FRONTEND=noninteractive \
    apt-get -y install \
    openssh-server \
    openssh-client

service ssh start
sed -i "s/^#\\(PasswordAuthentication\\)/\\1/" /etc/ssh/sshd_config
sed -i "s/^#\\(PermitRootLogin\\)/\\1/" /etc/ssh/sshd_config
sed -i "s/prohibit-password/yes/" /etc/ssh/sshd_config
sed -i "s/^Include/#&/" /etc/ssh/sshd_config
sed -i "s/^#\\(HostKey \\/etc\\/ssh\\/ssh_host_rsa_key\\)/\\1/" /etc/ssh/sshd_config
sed -i "s/^#\\(HostKey \\/etc\\/ssh\\/ssh_host_ed25519_key\\)/\\1/" /etc/ssh/sshd_config
service ssh restart

cp -R "/etc/ssh/" "$ip2key_path/$host_ip"
'''

# 暂停容器的时候已经把密钥删除了，所以这时就没什么需要后续处理的了
destory_cmd = f'''
'''

sleep_cmd = f'''
{get_ip}
rm -R "$ip2key_path/$host_ip"
'''

weakup_cmd = f'''
{get_ip}
cp -R "/etc/ssh/" "$ip2key_path/$host_ip"
service ssh restart
'''

start_listening_cmd = '''
screen -dmS mitm ./ssh-mitm-2.2/start-mitm.sh
cd /home/ssh-mitm/
python3 -m http.server 8081 &
'''

forward_cmd = '''
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -t nat -A PREROUTING -p tcp -i eth0 --dport 22 -j DNAT --to {to_ipaddr}:22
iptables -t nat -A POSTROUTING -j MASQUERADE
'''

test_cmd = f'''
{get_ip}
echo "$host_ip"
echo 'hello'
echo $ip2key_path

echo 'zimarnt' > /LALALA
'''
