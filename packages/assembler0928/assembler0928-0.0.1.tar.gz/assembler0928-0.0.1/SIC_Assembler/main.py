from pprint import pprint
instruction_set = {
    "ADD": 0x18, "ADDF": 0x58, "AND": 0x40, "COMP": 0x28, "COMPF": 0x88,
    "DIV": 0x24, "DIVF": 0x64, "J": 0x3C, "JEQ": 0x30, "JGT": 0x34,
    "JLT": 0x38, "JSUB": 0x48, "LDA": 0x00, "LDB": 0x68, "LDCH": 0x50,
    "LDF": 0x70, "LDL": 0x08, "LDS": 0x6C, "LDT": 0x74, "LDX": 0x04,
    "LPS": 0xD0, "MUL": 0x20, "MULF": 0x60, "OR": 0x44, "RD": 0xD8,
    "RSUB": 0x4C, "SSK": 0xEC, "STA": 0x0C, "STB": 0x78, "STCH": 0x54,
    "STF": 0x80, "STI": 0xD4, "STL": 0x14, "STS": 0x7C, "STSW": 0xE8,
    "STT": 0x84, "STX": 0x10, "SUB": 0x1C, "SUBF": 0x5C, "TD": 0xE0,
    "TIX": 0x2C, "WD": 0xDC
}
 
pseudo_list = ["START", "END", "BYTE", "WORD", "RESB", "RESW"]
 
sym_table = {}
 
def is_instuction(code):
 	prase = code.split()
 	for i in prase:
 		if i in pseudo_list:
 			result = False
 			break
 		else:
 			result = True
 	return result
 		
def sym_table_establish(line, loctr):
	symbol = line.split()
	chk = len(symbol)
	if (chk == 3) and (symbol not in pseudo_list):
		sym_table.setdefault(symbol[0], "{:X}".format(loctr))

#LOC
loctr = 0
with open('source.txt', 'r') as f:
	for line in f.readlines():
		with open('loc.txt', 'a') as floc:
			code = line.split()
			instruction_chk = is_instuction(line)
			if line.startswith('.'):
				floc.write(line)

			elif instruction_chk == True:
				sym_table_establish(line, loctr)
				floc.write("{:X}".format(loctr) + '\t' + line)
				loctr += 3

			elif instruction_chk == False:
				sym_table_establish(line, loctr)

				if 'START' in code:
					loctr = int(code[2], 16)
					floc.write('\t' + line)
				
				elif  ('END' in code) and ('FIRST' in code):
					floc.write("{:X}".format(loctr) + '\t' + line)

				elif 'WORD' in code:
					floc.write("{:X}".format(loctr) + '\t' + line)
					loctr += 3

				elif 'RESW' in code:
					floc.write("{:X}".format(loctr) + '\t' + line)
					loctr += int(code[len(code)-1])*3

				elif 'RESB' in code:
					floc.write("{:X}".format(loctr) + '\t' + line)
					loctr += int(code[len(code)-1])

				elif 'BYTE' in code:
					floc.write("{:X}".format(loctr) + '\t' + line)
					loctr_add = code[len(code)-1].split('\'')
					if loctr_add[0] == 'C':
						loctr += len(loctr_add[1])
					elif loctr_add[0] == 'X':
						loctr += len(loctr_add[1])//2
pprint(sym_table)

#OBJECTCODE
with open('loc.txt', 'r') as f:
	for line in f.readlines():
		with open('objcode.txt', 'a') as fobj:
			line = line.strip('\n')
			code = line.split()
			code_len = len(code)
			if line.startswith('.'):
				fobj.write(line + '\n')
				continue

			instruction_chk = is_instuction(line)
			obj_p1 = ''
			obj_p2 = ''
			if instruction_chk:
				if ',X' not in code[code_len -1]:
					if 'RSUB' not in code[code_len -1]:
						obj_p1 = instruction_set[code[code_len -2]]
						obj_p2 = int(sym_table[code[code_len -1]], 16)
						fobj.write(line + '\t' + "{:02X}{:X}".format(obj_p1, obj_p2) + '\n')
					else:
						obj_p1 = instruction_set[code[code_len -1]]
						obj_p2 = 0
						fobj.write(line + '\t\t' + "{:02X}{:04X}".format(obj_p1, obj_p2) + '\n')
				else:
					obj_p1 = instruction_set[code[code_len -2]]
					obj_p2 = int(sym_table[code[code_len -1].rstrip(',X')], 16)
					obj_p2 = obj_p2 + 0x8000
					fobj.write(line + '\t' + "{:02X}{:X}".format(obj_p1, obj_p2) + '\n')
			else:
				if 'START' in code:
					fobj.write(line + '\n')
				
				elif 'END' in code:
					fobj.write(line + '\n')

				elif ('RESW' in code) or ('RESB' in code):
					fobj.write(line + '\n')

				elif 'WORD' in code:
					obj_p2 = int(code[code_len -1])
					fobj.write(line + '\t' + "{:06X}".format(obj_p2) + '\n')

				elif 'BYTE' in code:
					tmp = code[code_len -1].split('\'')
					if tmp[0] == 'C':
						for i in tmp[1]:
							obj_p2 += "{:X}".format(ord(i))
						fobj.write(line + '\t' + obj_p2 + '\n')
					elif tmp[0] == 'X':
						fobj.write(line + '\t' + tmp[1] + '\n')