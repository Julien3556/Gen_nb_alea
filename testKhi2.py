import os

def test_khi_2(data):
    n = len(data)
    khi2 = 0
    freq = [0] * 256

    for byte in data:
        freq[byte] += 1

    for i in range(256):
        khi2 = khi2 + ((freq[i] - (n/256))**2) / (n/256)

    return khi2

def interpreter_khi2(khi2_value, alpha=0.05):
    """
    Valeurs critiques pré-calculées pour ddl=255
    """
    
    valeurs_critiques = {
        0.10: (232.9, 277.0),  # 90% confiance
        0.05: (216.6, 293.2),  # 95% confiance
        0.01: (200.9, 310.5)   # 99% confiance
    }
    
    borne_inf, borne_sup = valeurs_critiques.get(alpha, valeurs_critiques[0.05])
    
    print(f"Khi-2 calcule: {khi2_value:.2f}")
    print(f"Valeur attendue: 255")
    print(f"Intervalle de confiance ({int((1-alpha)*100)}%): [{borne_inf:.1f}, {borne_sup:.1f}]")
    
    if borne_inf <= khi2_value <= borne_sup:
        print(f"OK - Les donnees semblent aleatoires")
        return True
    else:
        print(f"ERREUR - Les donnees ne semblent PAS aleatoires")
        return False

# Test
data = os.urandom(10000)
khi2 = test_khi_2(data)
interpreter_khi2(khi2)