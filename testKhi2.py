import os

def test_khi_2(data):
    """
    Calcule la statistique du test du khi-deux (χ²) pour vérifier l'uniformité.
    
    Args:
        data (bytes or list): Séquence d'octets à tester pour l'uniformité
    
    Returns:
        float: Statistique χ² calculée (plus proche de 255, plus proche de l'uniformité)
    """
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
    Interprète et affiche le résultat du test du khi-deux (χ²).

    Valeurs critiques pour ddl=255.

    Args:
        khi2_value (float): Statistique χ² calculée par test_khi_2()
        alpha (float): Niveau de signification (par défaut 0.05 pour 95% de confiance)
    
    Returns:
        bool: True si les données sont uniformes au niveau alpha, False sinon
    """
    
    valeurs_critiques = {
        0.10: (232.9, 277.0),  # 90% confiance
        0.05: (216.6, 293.2),  # 95% confiance
        0.01: (200.9, 310.5)   # 99% confiance
    }
    
    borne_inf, borne_sup = valeurs_critiques.get(alpha, valeurs_critiques[0.05])
    
    
    print(f"Intervalle de confiance ({int((1-alpha)*100)}%): [{borne_inf:.1f}, {borne_sup:.1f}]")
    print(f"Khi-2: {khi2_value:.2f}")

    if borne_inf <= khi2_value <= borne_sup:
        print(f"OK - Les donnees sont uniforme")
        return True
    else:
        print(f"ERREUR - Les donnees ne sont PAS uniforme")
        return False
