from os import PathLike
import sys
import socket
import time
import select




# message = sock.recv(2048)
# if (message):
# 	print(message.decode())
# tmp = "hello"
# sock.send(tmp.encode())
# time.sleep(60)
# sock.close()
# exit()

# konversi desimal ke binary
def convertToBin(s):
	dictionary = {'0' : "0000",
		'1' : "0001",
		'2' : "0010",
		'3' : "0011",
		'4' : "0100",
		'5' : "0101",
		'6' : "0110",
		'7' : "0111",
		'8' : "1000",
		'9' : "1001",
		'A' : "1010",
		'B' : "1011",
		'C' : "1100",
		'D' : "1101",
		'E' : "1110",
		'F' : "1111" }
	bin = ""
	for i in range(len(s)):
		bin = bin + dictionary[s[i]]
	return bin
	
# konversi binary ke decimal
def convertToDecimal(s):
	dictionary = {"0000" : '0',
		"0001" : '1',
		"0010" : '2',
		"0011" : '3',
		"0100" : '4',
		"0101" : '5',
		"0110" : '6',
		"0111" : '7',
		"1000" : '8',
		"1001" : '9',
		"1010" : 'A',
		"1011" : 'B',
		"1100" : 'C',
		"1101" : 'D',
		"1110" : 'E',
		"1111" : 'F' }
	hex = ""
	for i in range(0,len(s),4):
		ch = ""
		ch = ch + s[i]
		ch = ch + s[i + 1]
		ch = ch + s[i + 2]
		ch = ch + s[i + 3]
		hex = hex + dictionary[ch]
		
	return hex

# Binary to decimal conversion
def bin2dec(binary):
	
	binary1 = binary
	decimal, i, n = 0, 0, 0
	while(binary != 0):
		dec = binary % 10
		decimal = decimal + dec * pow(2, i)
		binary = binary//10
		i += 1
	return decimal

# Decimal to binary conversion
def dec2bin(num):
	res = bin(num).replace("0b", "")
	if(len(res)%4 != 0):
		div = len(res) / 4
		div = int(div)
		counter =(4 * (div + 1)) - len(res)
		for i in range(0, counter):
			res = '0' + res
	return res

def permute(k, tabel_permute_choice_1, n):
	permutation = ""
	for i in range(0, n):
		permutation = permutation + k[tabel_permute_choice_1[i] - 1]
	return permutation

# memindahkan digit binary ke belakang sesuai jumlah shift tiap round
def pindah_belakang(k, nth_shifts):
	s = ""
	for i in range(nth_shifts):
		for j in range(1,len(k)):
			s = s + k[j]
		s = s + k[0]
		k = s
		s = ""
	return k

# calculating xow of two strings of binary number a and b
def xor(a, b):
	ans = ""
	for i in range(len(a)):
		if a[i] == b[i]:
			ans = ans + "0"
		else:
			ans = ans + "1"
	return ans

# Table of Position of 64 bits at initial level: Initial Permutation Table
tabel_initial_permutaion = [58, 50, 42, 34, 26, 18, 10, 2,
							60, 52, 44, 36, 28, 20, 12, 4,
							62, 54, 46, 38, 30, 22, 14, 6,
							64, 56, 48, 40, 32, 24, 16, 8,
							57, 49, 41, 33, 25, 17, 9, 1,
							59, 51, 43, 35, 27, 19, 11, 3,
							61, 53, 45, 37, 29, 21, 13, 5,
							63, 55, 47, 39, 31, 23, 15, 7]

# tabel expansi
exp_d = [32, 1 , 2 , 3 , 4 , 5 , 4 , 5,
		6 , 7 , 8 , 9 , 8 , 9 , 10, 11,
		12, 13, 12, 13, 14, 15, 16, 17,
		16, 17, 18, 19, 20, 21, 20, 21,
		22, 23, 24, 25, 24, 25, 26, 27,
		28, 29, 28, 29, 30, 31, 32, 1 ]

# tabel permutasi
permutasi_tabel = [ 16, 7, 20, 21,
		29, 12, 28, 17,
		1, 15, 23, 26,
		5, 18, 31, 10,
		2, 8, 24, 14,
		32, 27, 3, 9,
		19, 13, 30, 6,
		22, 11, 4, 25 ]

# tabel sbox
sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
		[ 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
		[ 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
		[15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13 ]],
			
		[[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
			[3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
			[0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
		[13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9 ]],

		[ [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
		[13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
		[13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
			[1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12 ]],
	
		[ [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
		[13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
		[10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
			[3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14] ],
		
		[ [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
		[14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
			[4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
		[11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3 ]],
	
		[ [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
		[10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
			[9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
			[4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13] ],
		
		[ [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
		[13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
			[1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
			[6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12] ],
		
		[ [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
			[1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
			[7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
			[2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11] ] ]

# tabel invers permutasi
tabel_invers_permutasi = [ 40, 8, 48, 16, 56, 24, 64, 32,
			39, 7, 47, 15, 55, 23, 63, 31,
			38, 6, 46, 14, 54, 22, 62, 30,
			37, 5, 45, 13, 53, 21, 61, 29,
			36, 4, 44, 12, 52, 20, 60, 28,
			35, 3, 43, 11, 51, 19, 59, 27,
			34, 2, 42, 10, 50, 18, 58, 26,
			33, 1, 41, 9, 49, 17, 57, 25 ]

def encrypt(pt, array_key_binary, array_key_decimal):
	pt = convertToBin(pt)
	# print("Sebelum dilakukan initial permutation : ", pt)
	# Mengacak bit plain text dengan tabel Initial Permutation
	pt = permute(pt, tabel_initial_permutaion, 64)
	# print("Setelah dilakukan initial permutation : ", pt)
	
	# membagi hasil initial permutation menjadi 2 bagian kiri & kanan
	left = pt[0:32]
	right = pt[32:64]

	#loop 16 putaran
	for i in range(0, 16):
		# melakukan ekspansi bit dari 32 menjadi 48
		right_ekspansi = permute(right, exp_d, 48)
		
		# melakukan xor hasil ekspansi bit dengan key internal
		xor_x = xor(right_ekspansi, array_key_binary[i])

		# melakukan subsitusi dengan tabel sbox
		sbox_str = ""
		for j in range(0, 8):
			row = bin2dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
			col = bin2dec(int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
			val = sbox[j][row][col]
			sbox_str = sbox_str + dec2bin(val)
			
		# melakukan permutasi dgn tabel permutasi
		sbox_str = permute(sbox_str, permutasi_tabel, 32)
		
		# melakukan xor dengan hasil sbox dan permutasi
		result = xor(left, sbox_str)
		left = result
		
		# melakukan penukaran
		if(i != 15):
			left, right = right, left
		# print("Round ", i + 1, " : ", "Left : ", convertToDecimal(left), ", Right:  ", convertToDecimal(right), " ", array_key_decimal[i])
	
	# menggabungkan yg sebelah kiri dgn kanan
	hasil = left + right
	
	# melakukan invers permutasi
	cipher_text = permute(hasil, tabel_invers_permutasi, 64)
	return cipher_text

ENCRYPT_KEY = "AABB09182736CCDD"

def DES(plain_text,is_encrypt):

	key = convertToBin(ENCRYPT_KEY)

	tabel_permute_choice_1 = [57, 49, 41, 33, 25, 17, 9,
								1, 58, 50, 42, 34, 26, 18,
								10, 2, 59, 51, 43, 35, 27,
								19, 11, 3, 60, 52, 44, 36,
								63, 55, 47, 39, 31, 23, 15,
								7, 62, 54, 46, 38, 30, 22,
								14, 6, 61, 53, 45, 37, 29,
								21, 13, 5, 28, 20, 12, 4 ]

	# melakukan permute choice key 1
	key = permute(key, tabel_permute_choice_1, 56)

	# table round shift
	round_shift_table = [1, 1, 2, 2,
					2, 2, 2, 2,
					1, 2, 2, 2,
					2, 2, 2, 1 ]

	# memotong key dari 56 bit menjadi 48 bit
	tabel_permute_choice_2 = [14, 17, 11, 24, 1, 5,
								3, 28, 15, 6, 21, 10,
								23, 19, 12, 4, 26, 8,
								16, 7, 27, 20, 13, 2,
								41, 52, 31, 37, 47, 55,
								30, 40, 51, 45, 33, 48,
								44, 49, 39, 56, 34, 53,
								46, 42, 50, 36, 29, 32 ]

	# memecah 56 bit dari key menjadi 2 bagian
	left = key[0:28] # array_key_binary for RoundKeys in binary
	right = key[28:56] # array_key_decimal for RoundKeys in hexadecimal

	array_key_binary = []
	array_key_decimal = []
	for i in range(0, 16):
		# memindahkan bit ke belakang sesuai tabel round shift
		left = pindah_belakang(left, round_shift_table[i])
		right = pindah_belakang(right, round_shift_table[i])
		
		# menyatukan key sebelah kiri dan kanan
		combine_str = left + right
		
		# mengubah key yg 56 bit menjadi 48 bit
		round_key = permute(combine_str, tabel_permute_choice_2, 48)

		array_key_binary.append(round_key)
		array_key_decimal.append(convertToDecimal(round_key))
	cipher_text = plain_text
	plain_text = plain_text[:-1]
	if (is_encrypt):
		sys.stdout.write("--ENKRIPSI--\n")
		cipher_text = convertToDecimal(encrypt(plain_text, array_key_binary, array_key_decimal))
		sys.stdout.write("Encrypted Text: ")
		sys.stdout.write(cipher_text)
		sys.stdout.flush()
	else:
		sys.stdout.write("--DEKRIPSI--\n")
		array_key_binary_rev = array_key_binary[::-1]
		array_key_decimal_rev = array_key_decimal[::-1]
		cipher_text = convertToDecimal(encrypt(plain_text, array_key_binary_rev, array_key_decimal_rev))
		sys.stdout.write("Decrypted Text: ")
		sys.stdout.write(cipher_text)
		sys.stdout.write("\n")
		sys.stdout.flush()
	return cipher_text

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('20.121.18.52',5002))

while True:
	streams = [sys.stdin,sock]
	read_sockets,write_socket, error_socket = select.select(streams,[],[])
	for s in streams:
		if (s == sock):
			message = sock.recv(2048).decode()
			if (message != "You Are Connected to The Server."):
				tmp = message.split()
				plain_text = tmp[1]
				message = DES(plain_text,0)
			sys.stdout.write(message)
			sys.stdout.flush()
		else:
			message = sys.stdin.readline()
			tmp = "(You) " + message
			message = DES(message,1)
			sock.send(message.encode())
			sys.stdout.write(tmp)
			sys.stdout.write("\n")
			sys.stdout.flush()
sock.close()

main()
