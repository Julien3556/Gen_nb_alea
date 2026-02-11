def LCG(a, c, m, seed, nb_steps):
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