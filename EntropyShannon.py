import math


def entropie_shannon_octet(data):
    n = len(data)
    freq = [0] * 256

    for byte in data:
        freq[byte] += 1

    H = 0
    for count in freq:
        if count > 0:
            p = count / n
            H -= p * math.log2(p)

    return H


def analyser_entropie(data):
    """
    Analyse rapide de l'entropie des données
    
    Returns:
        dict: Dictionnaire avec entropie, type de données estimé, et compression possible
    """
    H = entropie_shannon_octet(data)
    
    if H > 7.8:
        print(f"OK - Les donnees sont Aleatoire/Chiffre")
    else:
        print(f"ERREUR - Les donnees ne sont pas Aleatoire/Chiffre")
    


