import os
from ctypes import *
import threading

listenfd = (c_int) # 定义一个C语言的整型变量，用于存储客户端的套接字描述符
server_listenfd = (c_int) # 定义一个C语言的整型变量，用于存储服务器端的套接字描述符
clientfd = (c_int) # 定义一个C语言的整型变量，用于存储客户端连接后返回的套接字描述符
server_recvbuf = c_char_p("0".encode()) # 定义一个C语言的字符指针变量，用于存储服务器端接收到的数据
client_recvbuf = c_char_p("0".encode()) # 定义一个C语言的字符指针变量，用于存储客户端接收到的数据
my_socket_lib_client = cdll.LoadLibrary("./client.so") # 加载客户端动态链接库文件，并创建一个对象
my_socket_lib_server = cdll.LoadLibrary("./server.so") # 加载服务器端动态链接库文件，并创建一个对象


def start_server(port):
    return my_socket_lib_server.start_server(c_int(port))  # 调用服务器端动态链接库中的start_server函数，传入端口号参数，并返回server_listenfd

def server_accept(server_listenfd):
    return my_socket_lib_server.server_accept(server_listenfd)  # 调用服务器端动态链接库中的server_accept函数，传入server_listenfd参数，并返回clientfd

def server_recv(clientfd, bufsize, server_recvbuf):
    return my_socket_lib_server.recv_server(clientfd, c_int(bufsize), server_recvbuf)  # 调用服务器端动态链接库中的recv_server函数，传入clientfd、缓冲区大小和server_recvbuf参数，并返回接收到数据的长度

def server_send(clientfd, sendstr):
    return my_socket_lib_server.send_server(clientfd, sendstr)  # 调用服务器端动态链接库中的send_server函数，传入clientfd和要发送数据参数，并返回发送成功与否

def close_accept(clientfd):
    return my_socket_lib_server.close_accept(clientfd)  # 调用服务器端动态链接库中的close_accept函数，传入clientfd参数，并关闭该连接

def close_listenfd(server_listenfd):
    return my_socket_lib_server.close_listenfd(server_listenfd)  # 调用服务器端动态链接库中close_listen函数，传入server_listen参数，并关闭该套接字


def client_send(listenfd, inputstr):
    return my_socket_lib_client.sendall(listenfd, c_char_p(inputstr))  # 调用客户端动态链接库中sendall函数，传入listenf和要发送数据参数，并返回发送成功与否

def start_client(port, addr):
    return my_socket_lib_client.start_server(c_int(port), c_char_p(addr))  # 调用客户端动态链接库中start_client函数，传入port和addr参数，并返回listenf


def client_recv(listenf, bufsize, client_recvbuf):
    return my_socket_lib_client.recvall(listenf, c_int(bufsize), client_recvbuf)  # 调用客户端动态链接库中recvall函数，传入listenf、缓冲区大小和client_recvbuf参数，并返回接收到数据长度


def client_close(listenf):
    return my_socket_lib_client.close_client(listenf)  # 调用客户端动态链接库中close_client函数，传入listenf参数，并关闭该套接字


def clientsendtalk(listenfd):
    while True:
        c = input()
        if c == "quit":
            break
        client_send(listenfd, c.encode())
    client_close(listenfd)
    return 0


def clientrecvtalk(listenfd):
    global client_recvbuf
    while True:
        pil = client_recv(listenfd, 32, client_recvbuf)
        if pil > 0:
            print("recv_buf == %s" % str(client_recvbuf.value.decode()))
            client_recvbuf = (c_char * 1024)("0".encode())


def start_run(addr):
    port = 7779
    while True:
        listenfd = start_client(port, addr.encode())
        print("建立连接中～～\n")
        if listenfd > 0:
            print("连接建立成功～\n")
            break
    threading.Thread(target=clientsendtalk, args=(listenfd,)).start()
    threading.Thread(target=clientrecvtalk, args=(listenfd,)).start()
