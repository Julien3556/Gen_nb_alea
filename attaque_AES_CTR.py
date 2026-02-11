"""
Attaque par réutilisation de nonce en AES-CTR
Inspiré de: https://www.seald.io/fr/blog/3-erreurs-courantes-quand-on-implemente-du-chiffrement
"""
import os
import hashlib


def xor_bytes(b1, b2):
    """XOR de deux séquences de bytes"""
    return bytes(a ^ b for a, b in zip(b1, b2))


def generer_keystream(cle, nonce, longueur):
    """
    Génère un keystream à partir d'une clé et d'un nonce
    Simule AES-CTR 
    """
    keystream = b''
    compteur = 0
    
    while len(keystream) < longueur:
        bloc = hashlib.sha256(cle + nonce + compteur.to_bytes(8, 'big')).digest()
        keystream += bloc
        compteur += 1
    
    return keystream[:longueur]


def chiffrer_ctr(message, cle, nonce):
    """Chiffre un message en mode CTR"""
    keystream = generer_keystream(cle, nonce, len(message))
    return xor_bytes(message, keystream)


def dechiffrer_ctr(chiffre, cle, nonce):
    """Déchiffre un message en mode CTR (identique au chiffrement)"""
    keystream = generer_keystream(cle, nonce, len(chiffre))
    return xor_bytes(chiffre, keystream)


# ============================================================================
# CAS 1 : On réutilise le nonce donc l'attaque réussit
# ============================================================================


print("CAS 1 : On réutilise le nonce")
cle = b'Une_cle_secrete'
nonce_reutilise = b'un_nonce_au_hasard'  

# On crée deux messages secrets
m1 = b'Message numero un avec secret'
m2 = b'Message numero deux important'
c1 = chiffrer_ctr(m1, cle, nonce_reutilise)
c2 = chiffrer_ctr(m2, cle, nonce_reutilise)

print(f"\nMessages originaux:")
print(f"m1 = {m1}")
print(f"m2 = {m2}")

print(f"\nMessages chiffrés:")
print(f"c1 = {c1.hex()}")
print(f"c2 = {c2.hex()}")








xor_chiffres = xor_bytes(c1, c2)
xor_messages = xor_bytes(m1, m2)

print(f"\nXOR(c1, c2) = {xor_chiffres.hex()}")
print(f"XOR(m1, m2) = {xor_messages.hex()}")



def est_reussit():
    reussi = False
    if xor_chiffres == xor_messages:
        reussi = True
        print("\nL'attaque est réussi : notre message XOR(c1, c2) est égale à XOR(m1, m2)")
    else:
        print("\nL'Attaque à échouée")
    return reussi
est_reussit()



# Known-plaintext attack
print("\nOn teste si l'attaquant en connaissant m1, peut récupérer m2")

m2_recupere = xor_bytes(xor_chiffres, m1)
print(f"m2 récupéré = {m2_recupere}")
print(f"m2 original = {m2}")

def attaque_reussi():
    reussi = False
    if m2_recupere == m2:
        reussi = True
        print("\nSUCCÈS TOTAL : m2 complètement déchiffré sans la clé !")
    else:
        print("\nÉchec")
    return reussi
attaque_reussi()



# ============================================================================
# CAS 2 : On réutilise pas les nonces cette fois 
# ============================================================================



print('\n*********************************************************************')
print("CAS 2 : NONCES UNIQUES (SÉCURISÉ)")
nonce1 = os.urandom(8)
nonce2 = os.urandom(8) #Permet de créer des onces aléatoire(enfin assez uniques pour tester notre code)

print(f"\nNonce 1 : {nonce1.hex()}")
print(f"Nonce 2 : {nonce2.hex()}")

# On chiffrement avec des nonces cette fois si différents
c1_secure = chiffrer_ctr(m1, cle, nonce1)
c2_secure = chiffrer_ctr(m2, cle, nonce2)

print(f"\nMessages chiffrés:")
print(f"c1 = {c1_secure.hex()}")
print(f"c2 = {c2_secure.hex()}")


print("On tente maintenant l'attaque")
xor_chiffres_secure = xor_bytes(c1_secure, c2_secure)
xor_messages_expected = xor_bytes(m1, m2)

print(f"\nXOR(c1, c2) = {xor_chiffres_secure.hex()}")
print(f"XOR(m1, m2) = {xor_messages_expected.hex()}")


def attaque_echou():
    if xor_chiffres_secure != xor_messages_expected:
        print("\nL'attaque échoue les nonces protègents bel et bien les messages !")
    else:
        print("\nImpossible logiquement")

attaque_echou()
