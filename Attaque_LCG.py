"""
Attaque sur LCG par récupération de graine
Sources :
https://github.com/ajuelosemmanuel/Truncated_LCG_Seed_Recovery/blob/main/attack_exemple_lsb.py
https://payatu.com/blog/stream-ciphers-cryptography-for-ctfs/#LCG_Linear_Congruential_Generators
"""
import LCG



# X_n = (a * X_n + c) % m

def encrypt_LCG(plaintext,seed):
    """
    Chiffre un texte clair en utilisant un générateur LCG avec XOR.
    
    La fonction génère une suite LCG et effectue un XOR entre chaque octet du clair
    et l'octet correspondant de la suite LCG.
    
    Args:
        plaintext (str or list): Texte clair à chiffrer (peut être une chaîne ou liste d'entiers)
        seed (int): Graine initiale pour le générateur LCG
    
    Returns:
        list: Liste des octets chiffrés
    """
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
    """
    Déchiffre un texte chiffré en utilisant le même générateur LCG avec XOR.
    
    Cette fonction effectue une opération inverse du chiffrement en générant la même suite LCG
    et en appliquant l'opération XOR entre chaque octet chiffré et l'octet correspondant de la suite.
    
    Args:
        cyphertext (list): Liste des octets chiffrés
        seed (int): Graine initiale pour le générateur LCG (doit être la même que pour le chiffrement)
    
    Returns:
        list: Liste des octets déchiffrés
    """
    print("Dechiffrage du chiffre : ",cyphertext)
    X = LCG.LCG(a, c, m, seed, len(cyphertext))
    # print(X)
    plaintext = []
    for i in range(len(cyphertext)) :

        cyphertext_value = cyphertext[i]
        X_i = X[i]

        plaintext.append((cyphertext_value^X_i)%m)
    return plaintext

def euclide_etendu(b,n):
    """
    Calcule l'inverse modulaire de b modulo n en utilisant l'algorithme d'Euclide étendu.
    
    L'algorithme d'Euclide étendu permet de trouver l'inverse multiplicatif de b modulo n,
    c'est-à-dire un nombre t tel que (b * t) % n = 1. Cette fonction retourne None si l'inverse n'existe pas.
    
    Args:
        b (int): L'entier dont on cherche l'inverse modulaire
        n (int): Le modulo
    
    Returns:
        int or None: L'inverse modulaire de b modulo n, ou None si l'inverse n'existe pas
    """
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
    
def attack(cyphertext, plaintext_know):
    """
    Attaque par texte clair connu pour retrouver les paramètres du LCG.
    
    L'attaquant connaît le début du texte clair correspondant aux premiers octets du chiffré.
    
    Args:
        cyphertext (list): Liste des octets chiffrés
        plaintext_know (list or str): Début du texte clair (plaintext) pour les premiers octets
    
    Returns:
        tuple: (a_search, c_search) les paramètres retrouvés du LCG
    """

    # On calcul le début de la suite X du LCG
    X_find = []
    for i in range(len(plaintext_know)):
        key = (cyphertext[i]^plaintext_know[i]%m)
        X_find.append(key)
    print("Debut de la suite LCG : ",X_find)
    a_search = (X_find[2] - X_find[1]) * euclide_etendu(X_find[1] - X_find[0], m) % m
    c_search = (X_find[1] - X_find[0]*a_search) % m
    return a_search, c_search

if __name__ == "__main__":
    # Paramètres secrets
    a = 1103575245
    c = 12345
    m = 2**31
    seed = 12345
    print(f"Parametres secrets a : {a} et c : {c}")
    # Chiffrage
    plaintext = "CTF{flag}"
    cyphertext = encrypt_LCG(plaintext,seed)
    print("chiffre : ",cyphertext)
    print("\n")

    # Déchiffrage
    plaintext = decrypt_LCG(cyphertext,seed)
    print("Clair en ASCII : ",plaintext)
    print("Clair : ",end="")
    for el in plaintext:
        print(chr(el),end="")
    print("\n")

    # Simulation d'attaque
    print("Simulation d'attaque...")
    plaintext_know = plaintext[:3]
    print("Clair connu par l'attaquant : ",plaintext_know)
    (a_search,c_search)=attack(cyphertext, plaintext_know)
    print("a = ",a_search)
    print("c = ",c_search)