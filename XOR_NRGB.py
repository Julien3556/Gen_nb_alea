import random

def source_mauvaise(n, p):
    """
    Génère une source de bits biaisée avec une probabilité p pour le bit 1.
    
    Args:
        n (int): Nombre de bits à générer
        p (float): Probabilité d'obtenir un bit égal à 1 (entre 0 et 1)
    
    Returns:
        list: Liste de n bits (0 ou 1) générés avec probabilité p de 1
    """
    resultats = []
    for _ in range(n):
        tirage = random.random()
        if tirage < p:
            resultats.append(1)
        else:
            resultats.append(0)
    return resultats

def xor_sources(*sources):
    """
    Effectue une opération XOR sur plusieurs sources de bits.
    
    Args:
        *sources (tuple of lists): Sources de bits à combiner (chaque source doit avoir la même longueur)
    
    Returns:
        list: Liste contenant le résultat du XOR de toutes les sources, bit par bit
    """
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