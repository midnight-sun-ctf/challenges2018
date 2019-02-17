#include "VirtualMachine.h"

////
// PUBLIC METHODS
////

VirtualMachine::VirtualMachine(unsigned char* buf, size_t size) {
	program_buffer	= buf;
	program_size	= size;

#ifdef DBG
	std::cerr << "Loading program\n";
#endif

	hdr = (vp_header*)program_buffer;

	// size must be larger than header
	if (size < 12)
		goto ERROR;

	// check magic bytes
#ifdef DBG
	std::cerr << "Verifying magic... ";
#endif
	if (hdr->magic != 0x7076)
		goto ERROR;
	
	if (hdr->data_off > size || hdr->data_off == 0)
		goto ERROR;
	if (hdr->text_off > size || hdr->text_off == 0)
		goto ERROR;
	
	data_seg = program_buffer + hdr->data_off;
	text_seg = program_buffer + hdr->text_off;

#ifdef DBG
	std::cerr << "OK!\n";
	dump_header();
#endif

	// success!
	error = 0;
	return;

ERROR:
#ifdef DBG
	std::cerr << "\nAn error occurred when loading program\n";
#endif
	error = 1;
	return;
}

#ifdef DBG
void VirtualMachine::dump_header() {
	std::cerr << "Dumping VP header:\n";
	std::cerr << "magic: " << hdr->magic << "\n";
	std::cerr << "data_off: " << hdr->data_off << "\n";
	std::cerr << "text_off: " << hdr->text_off << "\n";
}
#endif

#ifdef DBG
void VirtualMachine::dump_state() {
	std::cerr << "Dumping VM state:\n";
	std::cerr << "\tip: " << (void*)ip << "\n";
	for (int i = 0; i < NUM_REGS; i++)
		std::cerr << "\tr" << i << ": " << regs[i] << "\n";
	std::cerr << "\tin_text(ip): " << in_text(ip) << "\n";
	std::cerr << "\terror: " << error << "\n";
}
#endif

int VirtualMachine::run() {
	// check error level
	if (error > 0) {
		return 0;
	}

	// clear registers
	for (int i = 0; i < NUM_REGS; i++)
		regs[i] = 0;

	ip = get_entry();

#ifdef DBG
	// Had off-by-one here, not sure why
	while (in_text(ip+1)) {
		/* Interactive loop */
		char cmd[128];
		printf("~> ");
		fflush(stdout);
		cmd[read(0, cmd, sizeof(cmd)-1)-1] = '\0';
		if (strcmp(cmd, "help") == 0) {
			printf("commands: step, state, run\n");
		} else if (*cmd == '\0' || strcmp(cmd, "step") == 0) {
			if (!single_step()) {
				dump_state();
				return 0;
			}
		} else if (strcmp(cmd, "state") == 0) {
			dump_state();	
		} else if (strcmp(cmd, "run") == 0) {
			break;
		} else {
			printf("unknown command: %s\n", cmd);
		}
	}
#endif

	while(in_text(ip+1)) {
		if (!single_step()) {
#ifdef DBG
			dump_state();
#endif
			return 0;
		}
	}

	return 1;
}

////
// PRIVATE METHODS
////
int VirtualMachine::single_step() {
	unsigned char opcode = next_uchar();
	//printf("opcode: 0x%x offs: 0x%x\n", opcode, ip-1-program_buffer-hdr->text_off);
	switch (opcode) {
	case 0: // nop
#ifdef DBG
		std::cerr << "nop\n";
#endif
		break;

	case 10: // goto
#ifdef DBG
		std::cerr << "goto\n";
#endif
		handle_goto();
		break;
	case 11: // gotoeq
#ifdef DBG
		std::cerr << "gotoeq\n";
#endif
		handle_gotoeq();
		break;
	case 12: // gotogt
#ifdef DBG
		std::cerr << "gotogt\n";
#endif
		handle_gotogt();
		break;
	case 13: // movmr
#ifdef DBG
		std::cerr << "movmr\n";
#endif
		handle_movmr();
		break;
	case 14: // movrm
#ifdef DBG
		std::cerr << "movrm\n";
#endif
		handle_movrm();
		break;
	case 15: // movrr
#ifdef DBG
		std::cerr << "movrr\n";
#endif
		handle_movrr();
		break;
	case 16: // addrr
#ifdef DBG
		std::cerr << "addrr\n";
#endif
		handle_addrr();
		break;
	case 17: // subrr
#ifdef DBG
		std::cerr << "subrr\n";
#endif
		handle_subrr();
		break;
	case 18: // xorrr
#ifdef DBG
		std::cerr << "xorrr\n";
#endif
		handle_xorrr();
		break;
	case 19: // putc
#ifdef DBG
		std::cerr << "putc\n";
#endif
		handle_putc();
		break;
	case 20: // getc
#ifdef DBG
		std::cerr << "getc\n";
#endif
		handle_getc();
		break;

	default:
#ifdef DBG
		std::cerr << "Undefined opcode '" << (uint8_t)*ip << "'\n";
#endif
		return 0;
	}
	return 1;
}

////
// OPCODE HANDLERS
////

void VirtualMachine::handle_goto() {
	goto_off(next_uint());
}

void VirtualMachine::handle_gotoeq() {
	auto off = next_uint();
	auto r2 = next_uchar();
	auto r1 = next_uchar(); 
	if (get_reg(r2) == get_reg(r1))
		goto_off(off);
}

void VirtualMachine::handle_gotogt() {
	auto off = next_uint();
	auto r2 = next_uchar();
	auto r1 = next_uchar(); 
	if (get_reg(r2) > get_reg(r1))
		goto_off(off);
}

void VirtualMachine::handle_movmr() {
	auto off = next_uint();
	auto reg = next_uchar();
	set_mem(off, get_reg(reg));
}

void VirtualMachine::handle_movrm() {
	auto reg = next_uchar();
	auto off = next_uint();
	set_reg(reg, get_mem(off));
}

void VirtualMachine::handle_movrr() {
	auto r2 = next_uchar();
	auto r1 = next_uchar();
	set_reg(r2, get_reg(r1));
}

void VirtualMachine::handle_addrr() {
	auto r2 = next_uchar();
	auto r1 = next_uchar();
	set_reg(r2, get_reg(r2) + get_reg(r1));
}

void VirtualMachine::handle_subrr() {
	auto r2 = next_uchar();
	auto r1 = next_uchar();
	set_reg(r2, get_reg(r2) - get_reg(r1));
}

void VirtualMachine::handle_xorrr() {
	auto r2 = next_uchar();
	auto r1 = next_uchar();
	set_reg(r2, get_reg(r2) ^ get_reg(r1));
}

void VirtualMachine::handle_putc() {
	putchar(get_reg(next_uchar()));
}

void VirtualMachine::handle_getc() {
	set_reg(next_uchar(), getchar());
}


int VirtualMachine::in_text(unsigned char* ptr) {
	return (ptr >= program_buffer + hdr->text_off &&
			ptr < program_buffer + program_size);
}

int VirtualMachine::in_data(unsigned char* ptr) {
	return (ptr >= program_buffer + hdr->data_off &&
			ptr < program_buffer + hdr->text_off);
}

unsigned char* VirtualMachine::get_entry() {
	return program_buffer + hdr->text_off;
}

void VirtualMachine::goto_off(uint32_t off) {
	ip = program_buffer + off;
}

uint32_t VirtualMachine::get_reg(unsigned char n) {
	if (n >= sizeof(regs)) {
#ifdef DBG
		std::cerr << "Failed to get register " << n << "\n";
#endif
		return 0;
	}
	return regs[n];
}
void VirtualMachine::set_reg(unsigned char n, uint32_t val) {
	if (n >= sizeof(regs)) {
#ifdef DBG
		std::cerr << "Failed to set register " << n << "\n";
#endif
		return;
	}
	regs[n] = val;
}

uint32_t VirtualMachine::get_mem(uint32_t off) {
	if (!in_data(program_buffer + off)) {
#ifdef DBG
		std::cerr << "Failed to get memory at offset " << off << "\n";
#endif
		return 0;
	}
	return *(uint32_t*)(program_buffer + off);
}

void VirtualMachine::set_mem(uint32_t off, uint32_t val) {
	if (!in_data(program_buffer + off)) {
#ifdef DBG
		std::cerr << "Failed to set memory at offset " << off << "\n";
#endif
		return;
	}
	*(uint32_t*)(program_buffer + off) = val;
}

unsigned char VirtualMachine::next_uchar() {
	unsigned char x = *ip;
	ip++;
	return x;
}

uint32_t VirtualMachine::next_uint() {
	uint32_t x = *(uint32_t*)ip;
	ip+=sizeof(uint32_t);
	return x;
}
