import os

def autocorrelation(data, lag):
    """
    Calcule l'autocorrélation pour un lag donné
    Résultat attendu pour données aléatoires: proche de 0
    Intervalle acceptable: [-3/√n, 3/√n]

    Args:
        data (list): Liste de nombres représentant la série temporelle
        lag (int): Décalage (nombre de positions) pour l'autocorrélation
    
    Returns:
        float: Coefficient d'autocorrélation normalisé entre -1 et 1
    """
    n = len(data)
    
    mean = sum(data) / n
    
    # Variance
    variance = sum((x - mean)**2 for x in data) / n
    
    # Autocorrélation
    covariance = 0
    for i in range(n - lag):
        covariance += (data[i] - mean) * (data[i + lag] - mean)
    
    covariance /= (n - lag)
    
    # Coefficient d'autocorrélation
    if variance == 0:
        return 0
    
    autocorr = covariance / variance
    return autocorr

def test_autocorrelation(data, lags=[1, 8, 16, 32]):
    """
    Teste l'autocorrélation.
    Calcule et affiche l'autocorrélation pour chaque décalage spécifié, en comparant
    le résultat au seuil acceptable basé sur la taille des données. Affiche aussi
    si chaque autocorrélation indique une corrélation significative ou pas.
    
    Args:
        data (list): Liste de nombres représentant la série temporelle à tester
        lags (list): Liste des décalages à tester (par défaut [1, 8, 16, 32])
    
    Returns:
        int: Retourne 0 si le test s'est déroulé correctement
    """
    n = len(data)
    seuil = 3 / (n ** 0.5)  
    
    print(f"Seuil acceptable: [{-seuil:.4f}, {seuil:.4f}]")
    print("")
    
    tous_ok = True
    for lag in lags:
        if lag >= n:
            print(f"Lag {lag}: SKIP (lag >= n)")
            continue
            
        autocorr = autocorrelation(data, lag)
        
        if abs(autocorr) < seuil:
            statut = "PAS DE CORRELATION"
        else:
            statut = "FORTE CORRELATION"
        
        print(f"Lag {lag:1d}: {autocorr:7.4f}  {statut}")
    
    print("") 
    return 0
