def LCG(a, c, m, seed, nb_steps):
    """
    Générateur de nombres pseudo-aléatoires utilisant le générateur congruential linéaire (LCG).
    
    Utilise la formule: X_n = (a * X_{n-1} + c) mod m
    
    Args:
        a (int): Paramètre multiplicateur
        c (int): Paramètre additif
        m (int): Paramètre modulo
        seed (int): Graine initiale
        nb_steps (int): Nombre d'itérations à générer
    
    Returns:
        list: Liste de nombres aléatoires générés par le LCG
    """
    X = []
    X_n = seed
    for i in range(nb_steps):
        X_n = (a * X_n + c) % m
        X.append(X_n)
    return X

if __name__ == "__main__":
    # Example de paramètres pour LCG utilisé par RANDU sur des machines IBM System/370
    # Ces paramètres sont biasés
    a = 65539
    c = 0
    m = 2**31
    seed = 7
    nb_steps = 100

    X = LCG(a, c, m, seed, nb_steps)
    print(X)