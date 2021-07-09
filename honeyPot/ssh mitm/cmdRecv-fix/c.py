import socket
from KeyAgreement import keyAgreementClient

TARGET_IP='0.0.0.0'
PORT=2333

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((TARGET_IP, PORT))
aesPipeIN, aesPipeOUT = keyAgreementClient(client)
print("Connected to Server.")

aesPipeOUT(input())
print(aesPipeIN())