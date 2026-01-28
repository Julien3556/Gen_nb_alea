def LCG(a, c, m, seed, nb_steps):
    X = []
    X_n = seed
    for i in range(nb_steps):
        X_n = (a * X_n + c) % m
        X.append(X_n)
    return X

if __name__ == "__main__":
    # Example parameters for the LCG
    a = 65539
    c = 0
    m = 2**31
    seed = 7
    nb_steps = 100

    X = LCG(a, c, m, seed, nb_steps)
    print(X)