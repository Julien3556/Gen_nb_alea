#Transformation de Box-Muller
import random
import math 


def box_muller():
    # Genere deux nombres aleatoires uniformes entre 0 et 1 sachant que 0 est exclu et 1 est inclus
    u1 = 1.0 - random.random()
    u2 = 1.0 - random.random()
    # Applique la transformation de Box-Muller
    z0 = (-2.0 * math.log(u1))**0.5 * (math.cos(2.0 * math.pi * u2))
    z1 = (-2.0 * math.log(u1))**0.5 * (math.sin(2.0 * math.pi * u2))
    return z0, z1

if __name__ == "__main__":
    z0, z1 = box_muller()
    print("Nombres aleatoires suivant une loi normale standard :")
    print(z0, z1)