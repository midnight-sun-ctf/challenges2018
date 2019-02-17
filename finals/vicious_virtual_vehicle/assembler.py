#!/usr/bin/env python

""" VP Assembler

output format:

      +-----------------+       : 0
      | magic(dw32)     |
      +-----------------+       : 4
      | data_offs(dw32) |---+
      +-----------------+   |   : 8
  +---| text_offs(dw32) |   |
  |   +-----------------+   |   : 12
  |   | data(arr)       |<--+   
  |   +-----------------+       : N/A
  +-->| text(arr)       |
      +-----------------+

 """
import struct
import sys

HEADER_SIZE = 12
HEADER_MAGIC= 'vp\x00\x00'

REGISTERS = {
	'r0':0,
	'r1':1,
	'r2':2,
	'r3':3,
	'r4':4
}

INSTR_LEN = {
	'nop':1,
	'goto':5,
	'gotoeq':7,
	'gotogt':7,
	'movmr':6,
	'movrm':6,
	'movrr':3,
	'addrr':3,
	'subrr':3,
	'xorrr':3,
	'putc':2,
	'getc':2
}

def _parse_meta(source):
	""" Parse and encode data segment in program
		param:		str:source
		return:		str:data_segment, dict:data_symbol_table, dict:text_symbol_table
	"""

	predicted_text_offset = 0

	print '[*] Parsing meta sequences'
	text_symbol_table={}
	data_symbol_table={}
	data_segment=''

	for line in source.split('\n'):
		tokens = line.split()
		if len(tokens) <= 0 or line.strip().startswith('#'): continue
		if tokens[0].lower() == 'var':
			print str(tokens)
			assert len(tokens) == 3, 'var <label> <value>'
			# currently only store data_segment offs for parsing later!
			data_symbol_table[tokens[1]] = len(data_segment)
			if tokens[2].startswith('0x'):
				val = int(tokens[2], 16)
			else:
				val = int(tokens[2])
			# add variable to data-segment
			data_segment += struct.pack('<I', val)

		elif tokens[0].lower() == 'lbl':
			assert len(tokens) == 2, 'lbl <name>'
			text_symbol_table[tokens[1]] = predicted_text_offset
		# Allows us to precompute labels
		elif tokens[0] in INSTR_LEN.keys():
			predicted_text_offset += INSTR_LEN[tokens[0]]

	print '[+] Parsing OK!'
	return data_segment, data_symbol_table, text_symbol_table

def _parse_text(source, text_offset, data_symbol_table, text_symbol_table):
	""" Parse and encode instructions in program 
		param:		str:source				program source code
		param:		int:text_offset			offset to text segment
		param:		dict:data_symbol_table	data symbol table
		param:		dict:text_symbol_table 	text symbol table
		return:		str:text_segment, dict:text_symbol_table
	"""

	print '[*] Parsing text segment'
	text_segment=''

	for line in source.split('\n'):
		tokens = line.split()

		# SKIP CONDITIONS
		if len(tokens) <= 0 or line.strip().startswith('#'): continue
		if tokens[0].lower() == 'var': # should already be handled
			continue

		print str(tokens)

		# INSTRUCTIONS
		if tokens[0] == 'nop':
			assert len(tokens) == 1, 'nop'
			text_segment += '\x00'

		elif tokens[0] == 'goto':
			assert len(tokens) == 2, 'goto <label>'
			assert tokens[1] in text_symbol_table.keys(), 'symbol %s not found' % tokens[1]
			text_segment += struct.pack('<BI', 10, 
										text_offset+text_symbol_table[tokens[1]])
		elif tokens[0] == 'gotoeq':
			assert len(tokens) == 4, 'gotoeq <label> <reg2> <reg1>'
			assert tokens[1] in text_symbol_table.keys(), 'symbol %s not found' % tokens[1]
			print tokens[2], tokens[3]
			assert tokens[2] in REGISTERS.keys() and tokens[3] in REGISTERS.keys(), 'invalid registers'
			text_segment += struct.pack('<BIBB', 11,
										text_offset+text_symbol_table[tokens[1]],
										REGISTERS[tokens[2]],
										REGISTERS[tokens[3]])
		elif tokens[0] == 'gotogt':
			assert len(tokens) == 4, 'gotogt <label> <reg2> <reg1>'
			assert tokens[1] in text_symbol_table.keys(), 'symbol %s not found' % tokens[1]
			assert tokens[2] in REGISTERS.keys() and tokens[3] in REGISTERS.keys(), 'invalid registers'
			text_segment += struct.pack('<BIBB', 12,
										text_offset+text_symbol_table[tokens[1]],
										REGISTERS[tokens[2]],
										REGISTERS[tokens[3]])
		elif tokens[0] == 'movmr':
			assert len(tokens) == 3, 'movmr <mem> <reg>'
			assert tokens[1] in data_symbol_table.keys(), 'symbol %s not found' % tokens[1]
			assert tokens[2] in REGISTERS.keys(), 'invalid registers'
			text_segment += struct.pack('<BIB', 13,
										HEADER_SIZE+data_symbol_table[tokens[1]],
										REGISTERS[tokens[2]])
		elif tokens[0] == 'movrm':
			assert len(tokens) == 3, 'movrm <reg> <mem>'
			assert tokens[1] in REGISTERS.keys(), 'invalid registers'
			assert tokens[2] in data_symbol_table.keys(), 'symbol %s not found' % tokens[1]
			text_segment += struct.pack('<BBI', 14,
										REGISTERS[tokens[1]],
										HEADER_SIZE+data_symbol_table[tokens[2]])
		elif tokens[0] == 'movrr':
			assert len(tokens) == 3, 'movrr <reg2> <reg1>'
			assert tokens[1] in REGISTERS.keys() and tokens[2] in REGISTERS.keys(), 'invalid registers'
			text_segment += struct.pack('<BBB', 15,
										REGISTERS[tokens[1]],
										REGISTERS[tokens[2]])
		elif tokens[0] == 'addrr':
			assert len(tokens) == 3, 'addrr <reg2> <reg1>'
			assert tokens[1] in REGISTERS.keys() and tokens[2] in REGISTERS.keys(), 'invalid registers'
			text_segment += struct.pack('<BBB', 16,
										REGISTERS[tokens[1]],
										REGISTERS[tokens[2]])
		elif tokens[0] == 'subrr':
			assert len(tokens) == 3, 'subrr <reg2> <reg1>'
			assert tokens[1] in REGISTERS.keys() and tokens[2] in REGISTERS.keys(), 'invalid registers'
			text_segment += struct.pack('<BBB', 17,
										REGISTERS[tokens[1]],
										REGISTERS[tokens[2]])
		elif tokens[0] == 'xorrr':
			assert len(tokens) == 3, 'xorrr <reg2> <reg1>'
			assert tokens[1] in REGISTERS.keys() and tokens[2] in REGISTERS.keys(), 'invalid registers'
			text_segment += struct.pack('<BBB', 18,
										REGISTERS[tokens[1]],
										REGISTERS[tokens[2]])

		elif tokens[0] == 'putc':
			assert len(tokens) == 2, 'putc <reg>'
			assert tokens[1] in REGISTERS.keys(), 'invalid registers'
			text_segment += struct.pack('<BB', 19,
										REGISTERS[tokens[1]])
		elif tokens[0] == 'getc':
			assert len(tokens) == 2, 'getc <reg>'
			assert tokens[1] in REGISTERS.keys(), 'invalid registers'
			text_segment += struct.pack('<BB', 20,
										REGISTERS[tokens[1]])
		
	print '[+] Parsing OK!'
	return text_segment, text_symbol_table

def parse_program(fname):
	data_symbol_table = {}
	text_symbol_table = {}
	data_segment=''
	text_segment=''

	with open(fname, 'r') as f:
		source = f.read()

	data_segment, data_symbol_table, text_symbol_table = _parse_meta(source)
	text_offset  = HEADER_SIZE + len(data_segment)
	text_segment, text_symbol_table = _parse_text(source, text_offset, data_symbol_table, text_symbol_table)
	
	print 'text_offset', text_offset

	# Building the final binary
	result = HEADER_MAGIC + struct.pack('<II', HEADER_SIZE, text_offset) + data_segment + text_segment

	return (data_symbol_table, 	# symbols pointing to data-segment
		    text_symbol_table, 	# symbols pointing to text-segment
		    data_segment,		# data segment content
		    text_segment,		# text segment content	
			result)		

def main(fname):
	data_symbol_table, text_symbol_table, data_segment, text_segment, program = parse_program(fname)
	# Print some bad debug info
	print 'data_symbol_table', data_symbol_table
	print 'text_symbol_table', text_symbol_table
	print 'data_segment', repr(data_segment)
	print 'text_segment', repr(text_segment)
	with open(fname.replace('.vp','.o'), 'wb') as f:
		f.write(program)

if __name__=='__main__':
	if len(sys.argv) > 1:
		main(sys.argv[1])
	else:
		print("Usage: %s <source.vp>" % sys.argv[0])
