import socket
import threading
import sys

class ChatClient:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"已连接到服务器 {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"连接服务器失败: {e}")
            return False

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"\n收到消息: {message}")
                print("请输入消息: ", end='', flush=True)
            except:
                print("\n与服务器的连接已断开")
                break

    def send_messages(self):
        while True:
            try:
                message = input("请输入消息: ")
                if message.lower() == 'quit':
                    break
                self.client_socket.send(message.encode('utf-8'))
            except:
                break

    def start(self):
        if not self.connect():
            return

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        self.send_messages()
        self.client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = 'localhost'
    
    client = ChatClient(host=host)
    client.start() 