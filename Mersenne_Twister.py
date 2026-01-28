
def int_to_bin(n):
    return bin(n)[2:]

def shift_right(n, bits):
    return n >> bits

def A(x):
    if x % 2 == 0:
        return shift_right(x, 1) ^ 0x00000000 # Xor avec 0
    else:
        return shift_right(x, 1) ^ 0x9908B0DF # Xor avec a = 2567483615
    

if __name__ == "__main__":
    n = 5
    binary = int_to_bin(n)
    print(f"Binaire de {n}: {binary}")

