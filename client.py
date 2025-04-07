import socket
import threading
import sys
import time

class ChatClient:
    def __init__(self, host='localhost', port=5001):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.username = None

    def connect(self):
        try:
            print(f"正在连接到服务器 {self.host}:{self.port}...")
            self.client_socket.connect((self.host, self.port))
            self.connected = True
            print(f"已成功连接到服务器 {self.host}:{self.port}")
            
            # 设置用户名
            while not self.username:
                self.username = input("请输入你的用户名: ").strip()
                if self.username:
                    self.client_socket.send(f"系统: {self.username} 加入了聊天室".encode('utf-8'))
                else:
                    print("用户名不能为空，请重新输入")
            
            return True
        except ConnectionRefusedError:
            print(f"连接失败: 无法连接到服务器 {self.host}:{self.port}")
            print("请检查:")
            print("1. 服务器是否已启动")
            print("2. 服务器地址和端口是否正确")
            print("3. 服务器和客户端是否在同一个网络中")
            return False
        except Exception as e:
            print(f"连接失败: {e}")
            return False

    def receive_messages(self):
        while self.connected:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"\n{message}")
                print("你: ", end='', flush=True)
            except:
                if self.connected:
                    print("\n与服务器的连接已断开")
                    self.connected = False
                break

    def send_messages(self):
        while self.connected:
            try:
                message = input("你: ")
                if not message.strip():
                    continue
                    
                if message.lower() == 'quit':
                    self.client_socket.send(f"系统: {self.username} 离开了聊天室".encode('utf-8'))
                    break
                    
                self.client_socket.send(f"{self.username}: {message}".encode('utf-8'))
            except:
                if self.connected:
                    print("发送消息失败")
                    self.connected = False
                break

    def start(self):
        if not self.connect():
            return

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        self.send_messages()
        self.connected = False
        self.client_socket.close()
        print("已断开与服务器的连接")

if __name__ == "__main__":
    # 解析命令行参数
    host = 'localhost'
    port = 5001
    
    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("端口号必须是数字")
            sys.exit(1)
    
    client = ChatClient(host=host, port=port)
    client.start() 