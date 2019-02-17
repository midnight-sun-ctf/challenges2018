#ifndef HAXDOOR_H
#define HAXDOOR_H

#include <stdint.h>

typedef void v0;
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef ssize_t sst;
typedef size_t st;

typedef struct {
	int fd;
} connection, *pconnection;


extern u32 g_timeout;
extern pthread_attr_t g_thread_attr;
extern connection g_con[10];
extern u32 g_con_num;

u32 login_handler(void);
u32 connectback(uint8_t *ip, uint32_t port);
v0 invite_handler(void *clientfd);
ssize_t recv_until(int fd, char *buf, size_t n, char marker);
ssize_t sendstr(int fd, const char *str);

#endif