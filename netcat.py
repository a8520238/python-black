import sys
import socket
import threading
import subprocess
import argparse

def serverloop():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))

    server.listen(5)

    while True:
        client_socket, _ = server.accept()
        print(client_socket)
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()


def client_sender(buffer):
    print("in_sender")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))
        if len(buffer):
            client.send(buffer.encode())

        while True:

            recv_len = 1
            response = ""

            while recv_len:

                data = client.recv(4096).decode()
                recv_len = len(data)
                response += data
                if recv_len < 4096:
                    break

            print (response)

            buffer = input("")
            buffer += "\n"

            client.send(buffer.encode())
    
    except:
        print("[*] Exception! Exiting")
        client.close()


def run_command(command):

    command = command.rstrip()
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command.\r\n"
    return output

def client_handler(client_socket):
    print("in_handle")
    if len(upload_destination):
        print("creating file")
        file_buffer = ""
        #while True:
            # data = client_socket.recv(1024).decode()

            # if not data:
            #     break

            # else:
            #     file_buffer += data
        file_buffer += client_socket.recv(1024).decode()
        print(file_buffer)
        try:
            file_name = open(upload_destination, "a")
            print(file_name)
            file_name.write(file_buffer)
            file_name.close()
            print("create file sucessfully")

            client_socket.send("Successfully saved file to {}\r\n".format(upload_destination).encode())

        except:
            client_socket.send("Failed to save file to {}\r\n".format(upload_destination).encode())

    if len(execute):
        output = run_command(execute)
        client_socket.send(output.encode())

    if command:
        print("in_command")
        while True:
            client_socket.send("<BHP:#> ".encode())

            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024).decode()
            response = run_command(cmd_buffer)
            print("response", response)
            client_socket.send(response)



if __name__ == "__main__":
    
    parser = argparse.ArgumentParser("BHP Net Tool")
    parser.add_argument("-l", "--listen", help="listen on [host] : [port] for incoming connections", default=False)
    parser.add_argument("-e", "--execute", help="execute the given file upon receiving a connection", default="")
    parser.add_argument("-c", "--command", help="initialize a command shell", default=False)
    parser.add_argument("-u", "--upload", help="upload a file and write to destination", default=False)
    parser.add_argument("-t", "--target", default="127.0.0.1")
    parser.add_argument("-up", "--upload_destination", default="")
    parser.add_argument("-p", "--port", default=80)
    args = parser.parse_args()

    listen = args.listen
    port = int(args.port)
    execute = args.execute
    command = args.command
    upload_destination = args.upload_destination
    target = args.target

    # decide listen or stdio send datas
    if not listen and len(target) and port > 0:
        buffer = sys.stdin.read()
        client_sender(buffer)
        
    if listen:
        serverloop()






