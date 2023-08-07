import socket

def start_client():
    host = "192.168.206.136" #選擇連接的server
    port = 12346 # and port

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print("Connected to C&C Server.")

    while True:
        # 接收來自Server的指令
        command = client_socket.recv(1024).decode()
        if command:
            print("Received command:", command)

            # 可以根據收到的指令，執行相應的操作
            # 在這個範例中，我們只是回應一個固定的訊息
            response = "Command executed successfully!"
            client_socket.send(response.encode())

    client_socket.close()

if __name__ == "__main__":
    start_client()