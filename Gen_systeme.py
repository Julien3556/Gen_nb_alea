import platform
import ctypes
import os

"""
On importe :
"platform" pour connaître le système d'exploitation de l'utilisateur,
"ctypes" pour importer les API de Windows et Linux,
"os" pour retourner les erreurs de l'API Linux.
"""

def urandom_linux(n):
    """
    Génère n octets aléatoires en utilisant la bibliothèque libc linux.
    
    Utilise la fonction getrandom de la libc Linux pour générer des nombres
    aléatoires cryptographiquement sécurisés.
    
    Args:
        n (int): Nombre d'octets aléatoires à générer
    
    Returns:
        bytes: Séquence de n octets aléatoires
    """
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
    Génère n octets aléatoires en utilisant l'API BCryptGenRandom de Windows.
    
    Utilise l'API crypt graphique native de Windows pour générer des nombres
    aléatoires de haute qualité via BCryptGenRandom.
    
    Args:
        n (int): Nombre d'octets aléatoires à générer
    
    Returns:
        bytes: Séquence de n octets aléatoires
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
        raise RuntimeError("L'API Windows BCryptGenRandom a echoue")

    return buffer.raw

def octets_to_int(octets):
    """
    Transforme les octets en entier.
    
    Convertit une séquence d'octets en un entier en utilisant l'ordre
    d'octet big-endian (poids fort d'abord).
    
    Args:
        octets (bytes): Octets générés aléatoirement
    
    Returns:
        int: Entier représentant les octets en base 256
    """
    return int.from_bytes(octets, byteorder="big")

def return_number():
    """
    
    Utilise la fonction main() pour générer 16 octets aléatoires,
    puis convertit ces octets en un entier.
    
    Args:
        None
    
    Returns:
        int: Nombre aléatoire entier généré à partir de 16 octets
    """
    n = main()
    seed = octets_to_int(n)
    return seed

def return_small_number():
    """
    
    Utilise la fonction main() pour générer 16 octets aléatoires,
    puis prend seulement le premier octet et le convertit en entier.
    
    Args:
        None
    
    Returns:
        int: Nombre aléatoire entier généré à partir d'un octet (valeur entre 0 et 255)
    """
    n = main()
    n = n[:1]
    seed = octets_to_int(n)
    return seed

def main():
    """
    Génère 16 octets aléatoires en utilisant l'API système appropriée.
    
    Détecte le système d'exploitation et utilise la méthode adéquate :
    - Linux : getrandom de libc
    - Windows : BCryptGenRandom
    - macOS et autres : non supportés
    
    Args:
        None
    
    Returns:
        bytes: 16 octets aléatoires générés de manière sécurisée
    """
    os_type = platform.system()

    if os_type == "Linux":
        # print("Systeme: Linux")
        n = urandom_linux(16)
    elif os_type == "Windows":
        # print("Systeme: Windows")
        n = urandom_windows(16)
    elif os_type == "Darwin":
        print("Systeme: macOS non supporte")
    else:
        print(f"Systeme: {os_type} non supporte")
    return n

if __name__ == "__main__":
    # Nombre aléatoire via os.urandom
    nb_aleatoire_urandom = os.urandom(16)

    # Nombre aléatoire de mon programme
    nb_aleatoire_octets = main()
    print(nb_aleatoire_octets)
    nb_aleatoire_int = octets_to_int(nb_aleatoire_octets)
    print(nb_aleatoire_int)

    print(return_small_number())