'''
RC4 Encryption
---Symmetric Key Encryption
'''


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
        encrypted.append(ord(plaintext[n])^K)
    return encrypted

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
S = KSA(key)
cipher = PRGA(S,plaintext)
#print("cipher", cipher)
res = ""
for s in cipher:
    #print(hex(s).zfill(4))
    res+=(hex(s)[2:]).zfill(2)
print("Ciphertext is : ",res)