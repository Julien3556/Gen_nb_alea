"""
Sources :
https://github.com/ajuelosemmanuel/Truncated_LCG_Seed_Recovery/blob/main/attack_exemple_lsb.py
https://payatu.com/blog/stream-ciphers-cryptography-for-ctfs/#LCG_Linear_Congruential_Generators
"""
import LCG
# Example de paramètres pour LCG utilisé par RANDU sur des machines IBM System/370
# Ces paramètres sont biasés
a = 1103575245
c = 12345
m = 2**31
seed = 12345

# X_n = (a * X_n + c) % m
# 

def encrypt_LCG(plaintext,seed):
    print("Chiffrage du clair : ",plaintext)
    X = LCG.LCG(a, c, m, seed, len(plaintext))
    print("Suite X",X)
    cyphertext = []
    for i in range(len(plaintext)) :

        if isinstance(plaintext[i], int):
            plaintext_value = plaintext[i]
        else:
            plaintext_value = ord(plaintext[i])

        X_i = X[i]

        cyphertext.append((plaintext_value^X_i)%m)
    return cyphertext

def decrypt_LCG(cyphertext,seed):
    print("Déchiffrage du chiffré : ",cyphertext)
    X = LCG.LCG(a, c, m, seed, len(cyphertext))
    # print(X)
    plaintext = []
    for i in range(len(cyphertext)) :

        cyphertext_value = cyphertext[i]
        X_i = X[i]

        plaintext.append((cyphertext_value^X_i)%m)
    return plaintext

def euclide_etendu(b,n):
    n0 = n
    b0 = b 
    t0 = 0
    t = 1
    q = n0 // b0
    r = n0 - q * b0
    while r > 0:
        temp = t0 - q * t
        if temp >= 0:
            temp = temp % n
        else:
            temp = n - ((-temp) % n)
        t0 = t
        t = temp
        n0 = b0
        b0 = r
        q = n0 // b0
        r = n0 - q * b0
    if b0 != 1:
        #print("Pas inversible")
        return None
    else:
        #print("Inverse :", t)
        return t
    
def attack(cyphertext):
    """ Dans cette attaque, on part du principe que l'attaquant connaît le début du clair"""
    plaintext_know = [102, 108, 97]

    # On calcul le début de la suite X du LCG
    X_find = []
    for i in range(len(plaintext_know)):
        key = (cyphertext[i]^plaintext_know[i]%m)
        X_find.append(key)
    a_search = (X_find[2] - X_find[1]) * euclide_etendu(X_find[1] - X_find[0], m) % m
    c_search = (X_find[1] - X_find[0]*a_search) % m
    return a_search, c_search

if __name__ == "__main__":
    # Chiffrage
    cyphertext = encrypt_LCG("flag{demo}",seed)
    print("chiffré : ",cyphertext)
    print("\n")

    # Déchiffrage
    plaintext = decrypt_LCG(cyphertext,seed)
    print("Clair en ASCII : ",plaintext)
    print("Clair : ",end="")
    for el in plaintext:
        print(chr(el),end="")
    print("\n")

    # Simulation d'attaque
    (a_search,c_search)=attack(cyphertext)
    print("a = ",a_search)
    print("c = ",c_search)