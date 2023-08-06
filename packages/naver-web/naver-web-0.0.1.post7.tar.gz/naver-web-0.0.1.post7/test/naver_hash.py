from cryptography.fernet import Fernet
import codecs


def genEncrypter(value):
    key = codecs.encode(str(value).encode("UTF-8"), "base64")
    encrypter = Fernet(key)
    return encrypter


def encrypt(value, salt):
    encrypter = genEncrypter(salt)
    encrypted = encrypter.encrypt(value.encode("utf-8"))
    print(encrypted)
    return encrypted


def decrypt(encrypted, salt):
    encrypter = genEncrypter(salt)
    print(encrypted)
    decrypted = encrypter.decrypt(encrypted)
    print(decrypted)
    return decrypted


if __name__ == "__main__":
    value = "jcuevas123!" 
    pksalt = "1qazxsw23edcvfr45tgbnhy67ujm,ki8"
    salt = decrypt(encrypt('7eb0df666a7fae2b4672cd59dae68c10', pksalt), pksalt);
    print(value)
    encrypt(value, salt)
    decrypt(encrypt(value, salt), salt)
