'''
RC4 Encryption
---Symmetric Key Encryption---
'''


def dec_string(text):
    decrypt = ""
    for i in range(0,len(text),2):
        k = int(text[i:i+2],16)
        #print(k)
        decrypt += chr(k)
    return decrypt

def listToSttring(lst):
    text = ""
    for i in lst:
        #print(chr(i))
        text += chr(i)
    return text

def KSA(key):
    l = len(key)

    S = [i for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i%l])%256
        S[i], S[j] = S[j], S[i]

    return S

def PRGA(S,plaintext):
    i = j = 0
    encrypted = []
    for n in range(len(plaintext)):
        i = (i+1)%256
        j = (j+S[i])%256
        S[i],S[j] = S[j], S[i]
        K =  S[(S[i]+S[j])%256]
        #print(plaintext[n] , K)
        encrypted.append(ord(plaintext[n])^K)
    return encrypted

def encrypt(key,plaintext):
    S = KSA(key)
    cipher = PRGA(S,plaintext)
    #print("cipher", cipher)
    res = ""
    for s in cipher:
        #print(hex(s).zfill(4))
        res+=(hex(s)[2:]).zfill(2)
    #print("Ciphertext is : ",res)
    return res

def decrypt(key,plaintext):
    lst = dec_string(plaintext)
    #print(lst)
    S = KSA(key)
    dec_list = PRGA(S,lst)
    #print(dec_list)
    init = listToSttring(dec_list)
    #print(init)
    return init

'''
key = "Key"
plaintext = "Plaintext"
res = 0xBBF316E8D940AF0AD3

key = "Wiki"
plaintext = "pedia"
res = 0x1021BF0420

key = "Secret"
plaintext = "Attack at dawn"
res = 0x45A01F645FC35B383552544B9BF5
'''


key = input("Enter key : ")
plaintext = input("Enter plaintext : ")

key = [ord(s) for s in key]

encrypted = encrypt(key,plaintext)
print("Encrypted : ", encrypted)

decrypted = decrypt(key,encrypted)
print("Decrypted : ", decrypted)
