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

def affichage_ks(D, n, alpha=0.05):
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
    
    if D < valeur_critique:
        print(f"OK - Distribution uniforme (niveau {int((1-alpha)*100)}%)")
        return True
    else:
        print(f"ERREUR - Distribution non uniforme")
        return False
