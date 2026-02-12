import struct
from Autocorrelation import *
from BBS import *
from Box_Muller import *
from Gen_systeme import *
from HMAC_DRBG import *
from LCG import *
from Mersenne_Twister import *
from XOR_NRGB import *
from EntropyShannon import *

def BBS():
    seed = 123 
    bits = 32
    nombre_bit_alea = 32 
    nb = 1000
    res = bbs(bits, seed,nombre_bit_alea, nb)
    tous_les_octets = b''
    for i in range(len(res)):
        longueur = (res[i].bit_length() + 7) // 8
        octets = res[i].to_bytes(longueur, byteorder='big')
        tous_les_octets += octets
    analyser_entropie(tous_les_octets)

def Box_Muller():
    tous_les_octets = b''
    for i in range(1000):
        x1,x2 = box_muller()
        octets = struct.pack('f', x1)
        tous_les_octets += octets
        octets = struct.pack('f', x2)
        tous_les_octets += octets
    analyser_entropie(tous_les_octets)

def Gen_Systeme():
     octets = urandom_windows(1000)
     analyser_entropie(octets)

def HMAC_DRGB():
    drbg = HMAC_DRBG (entropy=os.urandom (64))
    octets = drbg.generate (1000)
    analyser_entropie(octets)   

def LCG_test():
    a = 65539
    c = 0
    m = 2**31
    seed = 7
    nb_steps = 1000
    X = LCG(a, c, m, seed, nb_steps)
    tous_les_octets = b''
    for i in range(len(X)):
        longueur = (X[i].bit_length() + 7) // 8
        octets = X[i].to_bytes(longueur, byteorder='big')
        tous_les_octets += octets
    analyser_entropie(tous_les_octets)

def Mersenne_Twister():
    marseenne_seed = 123  
    numbers = mersenne_twister(marseenne_seed, 1000)
    tous_les_octets = b''
    for i in range(len(numbers)):
        longueur = (numbers[i].bit_length() + 7) // 8
        octets = numbers[i].to_bytes(longueur, byteorder='big')
        tous_les_octets += octets
    analyser_entropie(tous_les_octets)

def XOR_NRGB():
    n = 8196

    G1 = source_mauvaise(n, p=0.7)      
    G2 = source_mauvaise(n, p=0.55)     
    G3 = source_mauvaise(n, p=0.5)  

    G_hybride = xor_sources(G1, G2, G3)

    octets = []
    for i in range(0, len(G_hybride), 8):
        groupe = G_hybride[i:i+8]
        valeur = int(''.join(map(str, groupe)), 2)
        octets.append(valeur)

    resultat = bytes(octets)
    analyser_entropie(resultat)

if __name__ == "__main__":
    print("---------Entropie de Shannon---------")
    print("BBS : ",end = "")
    BBS()
    print("")

    print("Box_Muller : ",end = "")
    Box_Muller()
    print("")

    print("Gen-Systeme : ",end = "")
    Gen_Systeme()
    print("")

    print("HMAC_DRGB : ",end = "")
    HMAC_DRGB()
    print("")

    print("LCG : ",end = "")
    LCG_test()
    print("")

    print("Mersenne_Twister : ",end = "")
    Mersenne_Twister()
    print("")

    print("XOR_NRGB : ",end = "")
    XOR_NRGB()