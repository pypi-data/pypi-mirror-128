from cryptography.fernet import Fernet
import codecs
import random

memory = list()


def checkIfSaltExists(salt):
    """Verifica si una clave de una instancia de Fernet ya existe

    Args:
        salt (str): Clave de la instancia encriptada.

    Returns:
        bool: True si la clave ya existe, False si no.
    """
    if salt in memory:
        return True
    else:
        return False


def getUnique(list):
    """Retorna una lista sin elementos repetidos

    Args:
        list (list): Lista a la cual se le aplicará la función.

    Returns:
        list: Lista sin elementos repetidos.
    """
    uniquelist = []
    listset = set(list)
    for item in listset:
        uniquelist.append(item)
    return uniquelist


def generate():
    """Retorna un hash aleatorio

    Args:
        memory (list): Lista a la cual se le aplicará la función.

    Returns:
        str: Hash aleatorio.
    """
    hash = random.getrandbits(128).to_bytes(16, "big").hex()
    # newlist = []
    # newlist.append(hash)
    # memory = getUnique(newlist)
    return hash


def genEncrypter(value):
    """Genera una instancia de Fernet con el valor de la clave

    Args:
        value (str): Clave de la instancia.

    Returns:
        Fernet: Instancia de Fernet con la clave.
    """
    key = codecs.encode(str(value).encode("UTF-8"), "base64")
    encrypter = Fernet(key)
    return encrypter


def encrypt(value, salt):
    """Encrypta un valor con una clave

    Args:
        value (str): Valor a encriptar.
        salt (str): Clave de la instancia.

    Returns:
        str: Valor encriptado.
    """
    encrypter = genEncrypter(salt)
    encrypted = encrypter.encrypt(value.encode("utf-8"))
    print(encrypted)
    return encrypted


def decrypt(encrypted, salt):
    """Decrypta un valor con una clave

    Args:
        encrypted (Fernet): Valor a desencriptar.
        salt (str): Clave de la instancia.

    Returns:
        str: Valor desencriptado.
    """
    try:
        encrypter = genEncrypter(salt)
        print(encrypted)
        decrypted = encrypter.decrypt(encrypted)
        print(decrypted)
        return decrypted
    except Exception as e:
        raise e



def sendsalt(pksalt):
    """Envia una clave de una instancia de Fernet

    Args:
        pksalt (str): Clave de la instancia Primitiva.

    Returns:
        str: Clave de la instancia encriptada.
    """
    salt = encrypt(generate(), pksalt)
    return salt
