#pragma once

#undef DBG

#include <stdint.h>
#include <cstdio>
#include <unistd.h>
#include <string.h>
#ifdef DBG
#include <iostream>
#endif

#define NUM_REGS 5

/* 
VM Specification:
	magic:			vp\x00\x00 : 0x7076 : dword
	data offset:	dword
	text offset:	dword

ISA:
	mem:	dword
	reg:	byte
	op:		byte

	0:  nop					  					op
	10: goto   (ip   = mem)     				op 	mem
	11: gotoeq (ip   = mem if reg2 == reg1)     op	mem		reg2	reg1
	12: gotogt (ip   = mem if reg2 >  reg1)		op	mem		reg2	reg1
	13: movmr  (mem  = reg )    				op 	mem 	reg
	14: movrm  (reg  = mem )    				op 	reg 	mem
	15: movrr  (reg2 = reg1)					op 	reg2 	reg1
	16: addrr  (reg2 += reg1)   				op	reg2	reg1
	17: subrr  (reg2 -= reg1)   				op	reg2	reg1
	18: xorrr  (reg2 ^= reg1)   				op	reg2	reg1
	19: putc   (putc(reg))						op	reg
	20: getc   (reg = getc())					op	reg
*/

typedef struct _vp_header {
	uint32_t magic;
	uint32_t data_off;
	uint32_t text_off;
} vp_header;

class VirtualMachine {
public:
	// create new vm for given program
	VirtualMachine(unsigned char*, size_t);

	void* text_seg;		// text segment pointer
	void* data_seg;		// data segment pointer

	// executes program at 'entry' label
	int run();
#ifdef DBG
	void dump_state();
	void dump_header();
#endif

private:
	vp_header* hdr;	// store header information

	unsigned char* program_buffer;	// main program buffer
	size_t program_size;			// program buffer size

	int error;						// error level

	unsigned char* ip;				// instruction pointer
	uint32_t regs[NUM_REGS];		// registers

	int single_step();				// takes one emulation step

	int in_text(unsigned char*);	// checks that addr is within text segment
	int in_data(unsigned char*);	// checks that addr is within data segment

	unsigned char* get_entry();		// fetches program entrypoint
	void goto_off(uint32_t);		// helper to go to a location by offset 

	// getter/setter for registers
	uint32_t get_reg(unsigned char);
	void set_reg(unsigned char, uint32_t);
	// getter/setter for memory loc
	uint32_t get_mem(uint32_t);
	void set_mem(uint32_t, uint32_t);
	// helpers for consuming data in text segment
	uint32_t next_uint();
	unsigned char next_uchar();

	// opcode handlers (assumes proper handler is called)
	void handle_goto();
	void handle_gotoeq();
	void handle_gotogt();
	void handle_movmr();
	void handle_movrm();
	void handle_movrr();
	void handle_addrr();
	void handle_subrr();
	void handle_xorrr();
	void handle_putc();
	void handle_getc();

};
