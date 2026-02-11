import random

def source_mauvaise(n, p):
    resultats = []
    for _ in range(n):
        tirage = random.random()
        if tirage < p:
            resultats.append(1)
        else:
            resultats.append(0)
    return resultats

def xor_sources(*sources):
    res = []
    for i in range(len(sources[0])):   
        bits = 0
        for j in range(len(sources)):
            bits += sources[j][i]      
        res.append(bits % 2)
    return res
if __name__ == "__main__":
    n = 2048

    G1 = source_mauvaise(n, p=0.7)      
    G2 = source_mauvaise(n, p=0.55)     
    G3 = source_mauvaise(n, p=0.5)   # n'est pas une source mauvaise vue que p=0.5  

    G_hybride = xor_sources(G1, G2, G3)

    def proportion(bits):
        return sum(bits) / len(bits)

    print("G1 (biaisee):", proportion(G1))
    print("G2 (biaisee):", proportion(G2))
    print("G3 (quasi aleatoire):", proportion(G3))
    print("Hybride XOR :", proportion(G_hybride))