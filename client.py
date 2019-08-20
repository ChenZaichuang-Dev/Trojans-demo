# -*- coding: UTF-8 -*-

import os
import re
import socket
import sys


class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip  # 待连接的远程主机的域名
        self.server_port = server_port
        self.buffer_size = 10240

    def connect(self):  # 连接方法
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.server_ip, self.server_port))
        while True:
            message = input('> ')  # 接收用户输入
            s.send(bytes(message, 'utf-8'))  # 发送命令
            data = s.recv(self.buffer_size)  # 接收数据
            if not data:
                break
            if re.search("^0001", data.decode('utf-8', 'ignore')):  # 判断数据类型
                print(data.decode('utf-8')[4:])
            else:  # 文件内容处理
                s.send("File size received".encode())  # 通知服务端可以发送文件了
                file_total_size = int(data.decode())  # 总大小
                received_size = 0
                f = open("new" + os.path.split(message)[-1], "wb")  # 创建文件
                while received_size < file_total_size:
                    data = s.recv(self.buffer_size)
                    f.write(data)  # 写文件
                    received_size += len(data)  # 累加接收长度
                    print("已接收:", received_size)
                f.close()  # 关闭文件
                print("receive done", file_total_size, " ", received_size)


if __name__ == '__main__':
    cl = Client('127.0.0.1', 8800)
    cl.connect()
    sys.exit()  # 退出进程
