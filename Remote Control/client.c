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

int start_server(int port,char* addr)
{

  

	// create socket
	int clientfd = socket(AF_INET, SOCK_STREAM, 0);
	if(-1 == clientfd) {
		printf("create socket error");
		return -1;
	}
	
	// connect server 
	struct sockaddr_in serveraddr;
	serveraddr.sin_family = AF_INET;
	serveraddr.sin_addr.s_addr = inet_addr(addr);;
        serveraddr.sin_port = htons(port);
	
	if(-1 == connect(clientfd, (struct sockaddr *)&serveraddr, sizeof(serveraddr))) {
		printf("connect error");
		return -1;
	}
	
    return clientfd;
}
int sendall(int clientfd,char *input)



{

	int i=0;
	int ret = send(clientfd,input, strlen(input), 0);
	return ret;

}
int recvall(int clientfd,int bufsize,char* recvBuf)
{

	// receive data
	
	int ret = recv(clientfd, recvBuf, bufsize, 0);
	
	return ret;

} 
int close_client(int clientfd)
{close(clientfd);
return 0;
}
