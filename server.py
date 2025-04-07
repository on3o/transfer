import socket
import threading
import sys
import netifaces

class ChatServer:
    def __init__(self, host='0.0.0.0', port=5001):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        self.lock = threading.Lock()

    def get_local_ips(self):
        """获取本机所有IP地址"""
        ips = []
        for interface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                for addr in addrs[netifaces.AF_INET]:
                    ip = addr['addr']
                    if not ip.startswith('127.'):  # 排除本地回环地址
                        ips.append(ip)
        return ips

    def start(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            # 显示服务器信息
            local_ips = self.get_local_ips()
            print("\n=== 服务器启动成功 ===")
            print(f"监听地址: 0.0.0.0:{self.port}")
            print("可通过以下地址连接:")
            for ip in local_ips:
                print(f"- {ip}:{self.port}")
            print("=====================\n")

            while True:
                try:
                    client_socket, address = self.server_socket.accept()
                    print(f"新客户端连接: {address[0]}:{address[1]}")
                    
                    with self.lock:
                        self.clients.append(client_socket)
                        print(f"当前在线客户端数: {len(self.clients)}")
                    
                    client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
                    client_thread.start()
                except Exception as e:
                    print(f"处理客户端连接时出错: {e}")
                    continue
        except Exception as e:
            print(f"服务器启动失败: {e}")
            sys.exit(1)
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket, address):
        try:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                
                print(f"收到来自 {address[0]}:{address[1]} 的消息: {message}")
                self.broadcast(message, client_socket, address)
        except Exception as e:
            print(f"客户端 {address[0]}:{address[1]} 断开连接: {e}")
        finally:
            with self.lock:
                if client_socket in self.clients:
                    self.clients.remove(client_socket)
                    print(f"客户端 {address[0]}:{address[1]} 已断开")
                    print(f"当前在线客户端数: {len(self.clients)}")
            client_socket.close()

    def broadcast(self, message, sender_socket, sender_address):
        with self.lock:
            for client in self.clients[:]:
                if client != sender_socket:
                    try:
                        client.send(f"{sender_address[0]}: {message}".encode('utf-8'))
                    except Exception as e:
                        print(f"发送消息失败: {e}")
                        if client in self.clients:
                            self.clients.remove(client)

if __name__ == "__main__":
    port = 5001
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("端口号必须是数字")
            sys.exit(1)
    
    server = ChatServer(port=port)
    server.start() 