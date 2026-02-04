import os
import math

def test_kolmogorov_smirnov(data):
    """
    Test de Kolmogorov-Smirnov pour vérifier l'uniformité
    
    Compare la distribution empirique à la distribution uniforme théorique
    """
    n = len(data)
    sorted_data = sorted(data)
    
    D = 0
    for i, valeur in enumerate(sorted_data):
        # Distribution empirique 
        F_empirique = (i + 1) / n
        
        # Distribution théorique uniforme pour [0, 255]
        F_theorique = (valeur + 1) / 256
        
        # Distance entre le théorique et l'empirique
        distance = abs(F_empirique - F_theorique)
        
        # Garder le maximum
        if distance > D:
            D = distance
    
    return D

def interpreter_ks(D, n, alpha=0.05):
    """
    Interprète le résultat du test KS
    
    Valeur critique pour alpha=0.05: c = 1.36 / sqrt(n)
    """
    
    # Valeurs critiques selon le niveau de confiance
    c_values = {
        0.10: 1.22,  # 90% confiance
        0.05: 1.36,  # 95% confiance
        0.01: 1.63   # 99% confiance
    }
    
    c = c_values.get(alpha, 1.36)
    valeur_critique = c / math.sqrt(n)
    
    print(f"Test de Kolmogorov-Smirnov")
    print(f"Taille echantillon: {n}")
    print(f"Statistique D: {D:.6f}")
    print(f"Valeur critique (alpha={alpha}): {valeur_critique:.6f}")
    
    if D < valeur_critique:
        print(f"OK - Distribution uniforme (niveau {int((1-alpha)*100)}%)")
        return True
    else:
        print(f"ERREUR - Distribution non uniforme")
        return False

print("Test avec os.urandom")
data_random = list(os.urandom(10000))
D = test_kolmogorov_smirnov(data_random)
interpreter_ks(D, len(data_random))

print("\nTest avec donnees biaisees")
data_biased = [min(int(abs(i % 100)), 255) for i in range(10000)]
D = test_kolmogorov_smirnov(data_biased)
interpreter_ks(D, len(data_biased))