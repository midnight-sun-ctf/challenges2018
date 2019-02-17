#ifndef ROUTER_H
#define ROUTER_H

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <regex.h>

#include "zlib.h"

#define MAX_MESSAGE_LEN 2048
#define MAX_RESP_LEN 52000

#define HEADER_CONTENT_LEN	  	"Content-Length: "
#define HEADER_SERVER 		  	"Server: 1337-HTTPD\r\n"
#define HEADER_LOCATION		  	"Location: /page?=info\r\n"
#define HEADER_LINE_END			"\r\n"
#define HEADER_END 				"\r\n"

#define REQUEST_OK	  			"HTTP/1.1 200 OK\r\n"
#define REQUEST_BAD   			"HTTP/1.1 400 Bad Request\r\n"
#define REQUEST_NOT_FOUND  		"HTTP/1.1 404 Not Found\r\n"
#define REQUEST_REDIR	  		"HTTP/1.1 302 Found\r\n"
#define REQUEST_ERROR	  		"HTTP/1.1 500 Error\r\n"
#endif /*ROUTER_H*/