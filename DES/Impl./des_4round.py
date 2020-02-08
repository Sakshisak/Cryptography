def hexToBin(plain_text) :
	res = ""
	for i in range(len(plain_text)) :
		if plain_text[i] == '0' :
			res += '0000'
		elif plain_text[i] == '1' :
			res += '0001'
		elif plain_text[i] == '2' :
			res += '0010'
		elif plain_text[i] == '3' :
			res += '0011'
		elif plain_text[i] == '4' :
			res += '0100'
		elif plain_text[i] == '5' :
			res += '0101'
		elif plain_text[i] == '6' :
			res += '0110'
		elif plain_text[i] == '7' :
			res += '0111'
		elif plain_text[i] == '8' :
			res += '1000'
		elif plain_text[i] == '9' :
			res += '1001'
		elif plain_text[i] == 'A' or plain_text[i] == 'a':
			res += '1010'
		elif plain_text[i] == 'B' or plain_text[i] == 'b':
			res += '1011'
		elif plain_text[i] == 'C' or plain_text[i] == 'c':
			res += '1100'
		elif plain_text[i] == 'D' or plain_text[i] == 'd':
			res += '1101'
		elif plain_text[i] == 'E' or plain_text[i] == 'e':
			res += '1110'
		elif plain_text[i] == 'F' or plain_text[i] == 'f' :
			res += '1111'
		i += 1
	return res

#Subkey generation function
def key_64to56(plain_text):
	key = ""
	key_parity_drop = [57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36,63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]
	for x in key_parity_drop:
		key += plain_text[x-1]
	#print(key)
	return key

def compress_56to48(key):
  subkey = ""
  p =  [14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]
  for x in p:
  	subkey+=key[x-1]
  return subkey

def circular_shift(key,shift):
  temp=""
  temp=key[shift:]+key[:shift]
  return temp

def gen_keys(key):  #input is 16bit string

	key = hexToBin(key)
	key = key_64to56(key)
	left,right = key[:28],key[28:]

	round_shift = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

	subkeys = list()

	for i in range(4):
		left_new = circular_shift(left, round_shift[i])
		right_new = circular_shift(right, round_shift[i])
		combined = left_new + right_new
		combined = compress_56to48(combined) #56 to 48
		subkeys.append(combined)
		left = left_new
		right = right_new

	return subkeys

########

def IP(plain_text):
	p = ""
	IP = [58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,62,54,46,38,30,22,14,6,64,56,48,40,32,24,16,8,57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7]
	for x in IP :
	  p += plain_text[x-1]
	#print(p)
	return p

def inv_IP(plain_text):
	inv = ""
	IP = [40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25]
	for x in IP:
		inv += plain_text[x-1]
	#print(inv)
	return inv

def expand(plain_text):
	temp = ""
	ExpTable = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]
	for x in ExpTable :
		temp += plain_text[x-1]
	#print(temp)
	return temp

def p_box(s_out):
  p_box = [16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]
  s_final = ""
  for x in p_box:
  	s_final += s_out[x-1]
  return s_final

def s_box(temp):  #temp is 48 bit output of  R^Key

	s_out = ""
	s = [
	# b1
	[
	[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
	[0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
	[4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
	[15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
	],

	# b2
	[
	[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
	[3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
	[0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
	[13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
	],

	# b3
	[
	[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
	[13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
	[13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
	[1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]

	],

	# b4
	[
	[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
	[13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
	[10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
	[3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
	],

	# b5
	[
	[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
	[14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
	[4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
	[11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
	],

	# b6
	[
	[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
	[10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
	[9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
	[4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]

	],

	# b7
	[
	[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
	[13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
	[1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
	[6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
	],

	# b8
	[
	[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
	[1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
	[7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
	[2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
	]
	]
	for i in range(8):
		j = int((temp[6*i] + temp[6*i+5]),2)
		k = int((temp[6*i + 1]+temp[6*i + 2]+temp[6*i + 3]+temp[6*i + 4]),2)
		#s_out += binToHex('{0:002b}'.format(s[i][j][k]))
		s_out += '{0:04b}'.format(s[i][j][k])
		#print(s_out)
		
	return s_out

def f(right, key):
	right = expand(right)
	temp = int(right,2) ^ int(key,2)
	temp = '{0:048b}'.format(temp)
	#print(temp)
	s_out = s_box(temp)
	#print(s_out)
	s_final = p_box(s_out)
	#print(s_final)
	return s_final

def encrypt(plain_text) :

	key = 'AABB09182736CCDD'
	plain_text = hexToBin(plain_text) #converting the 16-bit string to 64-bit binary string

	plain_text = IP(plain_text) # Input permutation applied

	L = plain_text[:32]
	R = plain_text[32:]

	#Key generation
	subkeys = gen_keys(key)

	for i in range(3):
		r_out = f(R, subkeys[i])
		out = int(r_out, 2) ^ int(L, 2)
		L = R
		R = '{0:032b}'.format(out)

	r_out = f(R, subkeys[3])
	out = int(r_out, 2) ^ int(L, 2)
	L = '{0:032b}'.format(out)

	#print(L)
	#print(R)

	output = inv_IP(L+R)
	#print(output)
	encrypted = hex(int(output,2))[2:]

	return encrypted

def decrypt(plain_text) :
	key = 'AABB09182736CCDD'
	plain_text = hexToBin(plain_text) #converting the 16-bit string to 64-bit binary string
	#print(plain_text)
	plain_text = IP(plain_text) # Input permutation applied

	L = plain_text[:32]
	R = plain_text[32:]

	#Key generation
	subkeys = gen_keys(key)

	for i in range(3):
		r_out = f(R, subkeys[3-i])
		out = int(r_out, 2) ^ int(L, 2)
		L = R
		R = '{0:032b}'.format(out)

	r_out = f(R, subkeys[0])
	out = int(r_out, 2) ^ int(L, 2)
	L = '{0:032b}'.format(out)

	#print(L)
	#print(R)

	output = inv_IP(L+R)
	#print(output)
	encrypted = hex(int(output,2))[2:]

	return encrypted

x = input()
y = encrypt(x)
print("Encryption : ",y)
#print("hextoBIn",hexToBin('303f9e2c18a04377'))
print("Decryption : ",decrypt(str(y)))