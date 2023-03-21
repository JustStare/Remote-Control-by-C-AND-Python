#include<stdio.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<unistd.h>
#include<netinet/in.h>
#include<string.h>
#include<unistd.h>
#include<fcntl.h>
#include<arpa/inet.h>
/*使用传统的套接字来实现文件的传输 这里面就不封装HEADER头了  */

int start_server(int port)
{
   // create socket
	int listenfd = socket(AF_INET, SOCK_STREAM, 0);
	if(-1 == listenfd) {
		printf("create socket error");
		return -1;
	}
	
	// bind port 
	struct sockaddr_in bindaddr;
	bindaddr.sin_family = AF_INET;
	bindaddr.sin_addr.s_addr = htonl(INADDR_ANY);
	bindaddr.sin_port = htons(port);
	if(-1 == bind(listenfd, (struct sockaddr *)&bindaddr, sizeof(bindaddr))) {
		printf("bind error");
		return -1;
	}
	
	// start listen
	if (listen(listenfd, 2) == -1) {
		printf("listem error");
		return -1;
	}
	
	
	return   listenfd;
	}


int server_accept(int listenfd){
		struct sockaddr_in clientaddr;
		socklen_t clientaddrlen = sizeof(clientaddr);
		
		// accept connection
		int clientfd = accept(listenfd, (struct sockaddr *)&clientaddr, &clientaddrlen);
		
		return clientfd;}
int recv_server(int clientfd,int bufsize,char* recvBuf){
		       	
			
			
			// receive data
			int ret = recv(clientfd, recvBuf, bufsize, 0);		
		return ret;
				
}
		
		
int send_server(int clientfd,char* recvBuf)
{	// send data
		int ret = send(clientfd, recvBuf, strlen(recvBuf), 0);

			return ret;
		}
int close_accept(int clientfd)
{
close(clientfd);
return 0;
}

int close_listenfd(int listenfd){
	//close socket
	close(listenfd);
	return 0;
}




