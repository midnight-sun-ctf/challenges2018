#ifndef CHALL_H
#define CHALL_H

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>

#define NAME_MAX_SIZE 500

typedef void v0;
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;

typedef struct {
	u32  id;
  u32  type;
  u32  price;
  v0  *name;
} *porder, order;


#endif