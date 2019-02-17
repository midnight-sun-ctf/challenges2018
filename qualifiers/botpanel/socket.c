#define _BSD_SOURCE
#include <sys/socket.h>
#include <sys/types.h>
#include <linux/filter.h>
#include <arpa/inet.h>
#include <linux/if_ether.h>
#include <stdlib.h>
#include <stdio.h>
#include <signal.h>
#include <grp.h>
#include <unistd.h>
#include <pwd.h>
#include <features.h>
#include <string.h>
#include <errno.h>
#include <pthread.h>

#include "botpanel.h"

#define ARRAY_SIZE(arr) (sizeof(arr) / sizeof(arr[0]))
#define BUF_SIZ			1024

ssize_t recvlen(int fd, char *buf, size_t n) {
    ssize_t rc = 0;
    size_t nread = 0;
    while (nread < n) {
        rc = recv(fd, buf + nread, n - nread, 0);
        if (rc == -1) {
            if (errno == EAGAIN || errno == EINTR) {
                continue;
            }
            return -1;
        }
        if (rc == 0) {
            break;
        }
        nread += rc;
    }
    return nread;
}

ssize_t recv_until(int fd, char *buf, size_t n, char marker) {
    ssize_t rc = 0;
    size_t nread = 0;
    char c[1] =  "";
    while (nread < n) {
        rc = recv(fd, c, 1, 0);
        if (rc == -1) {
            if (errno == EAGAIN || errno == EINTR) {
                continue;
            }
            return -1;
        }
        if (rc == 0) {
            break;
        }
        if(c[0] == marker){
        	break;
        }
        buf[nread] = c[0];
        nread += rc;
    }
    return nread;
}

ssize_t sendlen(int fd, const char *buf, size_t n) {
    ssize_t rc;
    size_t nsent = 0;
    while (nsent < n) {
        rc = send(fd, buf + nsent, n - nsent, 0);
        if (rc == -1) {
            if (errno == EAGAIN || errno == EINTR) {
                continue;
            }
            return -1;
        }
        nsent += rc;
    }
    return nsent;
}

ssize_t sendstr(int fd, const char *str) {
    return sendlen(fd, str, strlen(str));
}

u32 connectback(u8 *ip, u32 port)
{
	int rc = 0;
  struct sockaddr_in saddr = {0};
	int clientfd = 0;

	int addr_size = sizeof(struct sockaddr_in);
  clientfd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
  if (clientfd == -1) {
      _exit(rc);
  }

  saddr.sin_family = AF_INET;
  saddr.sin_addr.s_addr = inet_addr(ip);
  saddr.sin_port = htons(port);

  rc = connect(clientfd, (struct sockaddr *)&saddr , sizeof(saddr));
  if(rc < 0)
  {
  	printf("Failed to send invite to that IP! Disconnecting ...\n");
  	_exit(-1);
  }

  if(g_con_num > 1){
  	printf("Maximum invites sent!\n");
  }

  g_con_num++;
  
  void * ts = calloc(sizeof(pthread_t), 1);
  g_con[g_con_num].fd = clientfd;
  pthread_create(ts, &g_thread_attr, (void*)&invite_handler, (void*)&g_con[g_con_num]);
  return 0;
}