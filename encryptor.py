import base64
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad

_ENCODING = 'ISO-8859-1'


class Encryptor:
    @staticmethod
    def __get_private_key(passwd, salt) -> bytes:
        kdf = PBKDF2(passwd, salt, 64, 1000)
        return kdf[:32]

    @staticmethod
    def encrypt(data, passwd, salt="test_salt___") -> bytes:
        private_key = Encryptor.__get_private_key(passwd, salt.encode(_ENCODING, errors='replace'))
        raw = data.encode(_ENCODING, errors='replace')
        raw = pad(raw, AES.block_size)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    @staticmethod
    def encrypt_raw(raw, passwd, salt="test_salt___") -> bytes:
        private_key = Encryptor.__get_private_key(passwd, salt.encode(_ENCODING, errors='replace'))
        raw = pad(raw, AES.block_size)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    @staticmethod
    def decrypt(data, passwd, salt="test_salt___") -> str:
        private_key = Encryptor.__get_private_key(passwd, salt.encode(_ENCODING, errors='replace'))
        data = base64.b64decode(data)
        iv = data[:16]
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        return bytes.decode(unpad(cipher.decrypt(data[16:]), AES.block_size))

    @staticmethod
    def decrypt_raw(raw, passwd, salt="test_salt___") -> bytes:
        private_key = Encryptor.__get_private_key(passwd, salt.encode(_ENCODING, errors='replace'))
        raw = base64.b64decode(raw)
        iv = raw[:16]
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(raw[16:]), AES.block_size)

    @staticmethod
    def encrypt_file(path_to_encrypt, path_encrypted, password):
        old = open(path_to_encrypt, "r+b")
        new = open(path_encrypted, "x+b")
        bytes64 = old.read(64)
        while bytes64:
            encrypted_test = Encryptor.encrypt_raw(bytes64, password)
            bytes64 = old.read(64)
            new.write(encrypted_test)
        new.close()
        old.close()

    @staticmethod
    def decrypt_file(path_to_decrypt, path_decrypted, password):
        old = open(path_to_decrypt, "r+b")
        new = open(path_decrypted, "x+b")
        bytes128 = old.read(128)
        while bytes128:
            decrypted_test = Encryptor.decrypt_raw(bytes128, password)
            bytes128 = old.read(128)
            new.write(decrypted_test)
        new.close()
        old.close()
