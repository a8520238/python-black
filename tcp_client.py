import socket

target_host = "0.0.0.0"
target_port = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host, target_port))

str1 = "GET / HTTP/1.1\r\nHost: www.baidu.com\r\n\r\n"

client.send(str1.encode())

response = client.recv(4096).decode()

print(response)