import socket
import threading

class ChatServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.lock = threading.Lock()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"服务器启动成功，监听地址: {self.host}:{self.port}")

        while True:
            client_socket, address = self.server_socket.accept()
            print(f"新客户端连接: {address}")
            
            with self.lock:
                self.clients.append(client_socket)
            
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_thread.start()

    def handle_client(self, client_socket, address):
        try:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                
                print(f"收到来自 {address} 的消息: {message}")
                self.broadcast(message, client_socket)
        except:
            print(f"客户端 {address} 断开连接")
        finally:
            with self.lock:
                self.clients.remove(client_socket)
            client_socket.close()

    def broadcast(self, message, sender_socket):
        with self.lock:
            for client in self.clients:
                if client != sender_socket:
                    try:
                        client.send(message.encode('utf-8'))
                    except:
                        self.clients.remove(client)

if __name__ == "__main__":
    server = ChatServer()
    server.start() 