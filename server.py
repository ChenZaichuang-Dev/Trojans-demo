# -*- coding: UTF-8 -*-

import os
import socket


class Server:
    def __init__(self, ip, port):
        self.port = port
        self.ip = ip
        self.buffer_size = 10240

    def start(self):  # 启动监听，接收数据
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ip, self.port))  # 绑定
        s.listen(10)  # 监听
        print('等待客户端连接')
        try:
            while True:  # 一直等待新的连接
                conn, addr = s.accept()  # 接收连接
                print('客户端连接 ' + addr[0] + ':' + str(addr[1]))
                try:
                    while True:  # 保持长连接
                        data = conn.recv(self.buffer_size)  # 接收数据
                        self.execute_command(conn, data)
                except Exception:
                    pass
        finally:
            s.close()  # 关闭服务端

    def execute_command(self, tcp_client_sock, data):  # 解析并执行命令
        message = data.decode("utf-8")
        if os.path.isfile(message):  # 判断是否是文件
            file_size = str(os.path.getsize(message))  # 获取文件大小
            print("文件大小为：", file_size)
            tcp_client_sock.send(file_size.encode())  # 发送文件大小
            tcp_client_sock.recv(self.buffer_size)
            print("开始发送")
            f = open(message, "rb")  # 打开文件
            for line in f:
                tcp_client_sock.send(line)  # 发送文件内容
        else:
            tcp_client_sock.send(('0001' + os.popen(message).read()).encode('utf-8'))


if __name__ == '__main__':
    s = Server('', 8800)
    s.start()
