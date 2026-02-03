import ctypes
import os
import platform

def urandom_linux(n):
    # Charger libc
    libc = ctypes.CDLL("libc.so.6", use_errno=True)

    libc.getrandom.argtypes = [
        ctypes.c_void_p,
        ctypes.c_size_t,
        ctypes.c_uint
    ]
    libc.getrandom.restype = ctypes.c_ssize_t
    buf = ctypes.create_string_buffer(n)

    res = libc.getrandom(buf, n, 0)
    if res < 0:
        err = ctypes.get_errno()
        raise OSError(err, os.strerror(err))

    return buf.raw


def urandom_windows(n) :
    """
    Génère n octets aléatoires en utilisant l'API BCrypt de Windows.
    """

    # Charger la DLL Windows
    bcrypt = ctypes.WinDLL("bcrypt.dll")

    # Constante officielle définie par Microsoft
    BCRYPT_USE_SYSTEM_PREFERRED_RNG = 0x00000002
    
    buffer = ctypes.create_string_buffer(n)

    status = bcrypt.BCryptGenRandom(
        None,
        buffer,
        n,
        BCRYPT_USE_SYSTEM_PREFERRED_RNG
    )

    if status != 0:
        raise RuntimeError("L'API Windows BCryptGenRandom a échoué")

    return buffer.raw

def octets_to_int(octets):
    return int.from_bytes(octets, byteorder="big")

def main():
    os_type = platform.system()

    if os_type == "Linux":
        print("Systeme: Linux")
        n = urandom_linux(16)
        print(n)
    elif os_type == "Windows":
        print("Systeme: Windows")
        n = urandom_windows(16)
        print(n)
    elif os_type == "Darwin":
        print("Systeme: macOS non supporté")
    else:
        print(f"Systeme: {os_type} non supporté")
    return n

if __name__ == "__main__":
    # Nombre aléatoire via os.urandom
    nb_aleatoire_urandom = os.urandom(16)

    # Nombre aléatoire de mon programme
    nb_aleatoire_octets = main()
    print(nb_aleatoire_octets)
    nb_aleatoire_int = octets_to_int(nb_aleatoire_octets)
    print(nb_aleatoire_int)