import math
import os


def entropie_shannon_octet(data):
    """
    Calcule l'entropie de Shannon d'une séquence de bytes.
    
    L'entropie de Shannon mesure le degré d'incertitude ou de désordre dans les données.
    Pour des données parfaitement aléatoires de 256 octets distincts, l'entropie maximale
    est de 8 bits (log2(256) = 8). Une entropie plus basse indique des données moins aléatoires.
    
    Args:
        data (bytes): Séquence de bytes dont on calcule l'entropie
    
    Returns:
        float: Entropie de Shannon en bits, entre 0 et 8 pour des octets
    """
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

data = os.urandom(10000)  
print(entropie_shannon_octet(data))