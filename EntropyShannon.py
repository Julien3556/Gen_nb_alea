import math
import os


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

data = os.urandom(10000)  
print(entropie_shannon_octet(data))