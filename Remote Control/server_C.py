import threading
import os
from ctypes import *

listenfd = (c_int)
server_listenfd = (c_int)
clientfd = (c_int)
server_recvbuf = c_char_p("0".encode())
client_recvbuf = c_char_p("0".encode())
my_socket_lib_client = cdll.LoadLibrary("./client.so")
my_socket_lib_server = cdll.LoadLibrary("./server.so")


def start_server(port):
    return my_socket_lib_server.start_server(c_int(port))  # return server_listenfd


def server_accept(server_listenfd):
    return my_socket_lib_server.server_accept(server_listenfd)  # return clicentfd


def server_recv(clientfd, bufsize, server_recvbuf):
    return my_socket_lib_server.recv_server(clientfd, c_int(bufsize), server_recvbuf)


def server_send(clientfd, sendstr):
    return my_socket_lib_server.send_server(clientfd, c_char_p(sendstr))


def close_accept(clientfd):
    return my_socket_lib_server.close_accept(clientfd)


def close_listenfd(server_listenfd):
    return my_socket_lib_server.close_listenfd(server_listenfd)


def client_send(lintenfd, inputstr):
    return my_socket_lib_client.sendall(listenfd, c_char_p(inputstr))


def start_client(port, addr):
    return my_socket_lib_client.start_server(c_int(port), c_char_p(addr))


def client_recv(listenfd, bufsize, client_recvbuf):
    return my_socket_lib_client.recvall(listenfd, c_int(bufsize), client_recvbuf)


def client_close(listenfd):
    return my_socket_lib_client.close_client(listenfd)


def serversendtalk(clientfd):
    
    while True:
        s = input()
        if s == "quit()":
            break
        server_send(clientfd, s.encode())
    close_accept(clientfd)
    return 0
def serverrecvtalk(clientfd):
	global server_recvbuf
	while True:
            ret = server_recv(clientfd, 32, server_recvbuf)
            if ret > 0:
                print("recv_buf == %s" % str(server_recvbuf.value.decode()))
                server_recvbuf = c_char_p("0".encode())


def start_run():

    port = 7779
    server_listenfd = start_server(port)
    clientfd = server_accept(server_listenfd)

    threading.Thread(target=serversendtalk, args=(clientfd,)).start()	
    threading.Thread(target=serverrecvtalk, args=(clientfd,)).start()    
        
        
   #     while True:
    #        ret = server_recv(clientfd, 32, server_recvbuf)
     #       if ret > 0:
      #          print("recv_buf == %s" % str(server_recvbuf.value.decode()))
                
     #   c = input()
      #  if c == "quit":
       #     break
        #ret = server_send(clientfd, c.encode())
        #if ret > 0:
         #   print("send %s \n" % c)

