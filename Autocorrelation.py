import os

def autocorrelation(data, lag):
    """
    Calcule l'autocorrélation pour un lag donné
    Résultat attendu pour données aléatoires: proche de 0
    Intervalle acceptable: [-3/√n, 3/√n]
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
    Test d'autocorrélation 
    """
    n = len(data)
    seuil = 3 / (n ** 0.5)  # Seuil de signification à 95%
    
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


print("Test avec os.urandom")
data_random = list(os.urandom(10000))
test_autocorrelation(data_random)

print("\nTest avec pattern")
data_pattern = [i % 10 for i in range(10000)]  
test_autocorrelation(data_pattern)