# import socket

# target_host = "127.0.0.1"
# target_port = 1080

# client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# print("client is created")

# str1 = "AAABBBCCCC"

# client.sendto(str1.encode(), (target_host, target_port))

# print("data is sent")

# data, addr = client.recvfrom(10)

# print("data is got")

# print(data.decode())

# client.close()

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ("127.0.0.1", 6000)

while True:
    data = input("Please input your name: ")
    if not data:
        continue
    s.sendto(data.encode(), addr)
    response, addr = s.recvfrom(1024)
    print(response.decode())
    if data == "exit":
        print("Session is over from the server %s:%s\n" % addr)
        break

s.close()