'''
RSA Encryption

n = p*q should be greater than 128 for proper display of all characters.

'''
import random

def gcd(a,b):
    if (b==0):
        return a
    return gcd(b,a%b)

def isPrime(n): 
	if n <= 1: 
		return False
	for i in range(2, n): 
		if n % i == 0: 
			return False
	return True

def encrypt(msg,n,e): #returns a list of integers
    l = []
    #print(e,n)
    for c in msg:
        #print(ord(c))
        l.append(pow(ord(c),e,n))
    return l

def decrypt(msg,n,d): #returns a string
    #print(d,type(d),n,type(n))
    string2 = ""
    for c in msg:
        #print(pow(c,d,n))
        string2+=chr(pow(c,d,n))
    return string2

# p and q are two random prime numbers
p = int(input('Enter a prime number : '))
if(isPrime(p) == False):
    exit()
q = int (input('Enter another prime number : '))
if(isPrime(q) == False):
    exit()

# n is part of the public key
n = p*q
phi = (p-1)*(q-1)

# exponent part of the public key
e = int(random.randrange(1,phi))
# checking coprimality of e and phi
while(gcd(phi,e)!=1):
    e = int(random.randrange(1,phi))
#print("e is : ",e)

for k in range(1,1000): 
    x = 1 + k*phi
    if x % e == 0: 
        d = int(x/e)
        #print("k is : ",k)
        #print("d is : ", d)
        break

msg = input('Enter message to be encrypted : ')
encrypted = encrypt(msg,n,e)
print("Encrypted is : ", encrypted)
org = decrypt(encrypted,n,d)
print("Decrypted is : ", org)