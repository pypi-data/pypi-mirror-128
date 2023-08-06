import yaml
import string
import random
import os
import urllib.request
from pathlib import Path

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes

def resolvePath(path: str) -> str:
    return Path(path).expanduser().resolve()

class Model(dict):
    __getattr__ = dict.get
    __delattr__ = dict.__delitem__
    __setattr__ = dict.__setitem__

class Secrets(Model):
    def __init__(self, datafile="secrets",
            gh_user='baileywickham',
            public_key_file=None,
            private_key_file='~/.ssh/id_rsa',
            public_key=None,
            private_key=None):
        self.datafile : str = datafile
        self.datafile_enc : str = datafile + '.enc'

        self.gh_user : str = gh_user
        self.public_key_file : str = public_key_file
        self.private_key_file : str = private_key_file

        self.public_key : RSA = public_key
        self.private_key : RSA = private_key

        self.secrets = {}

        self.addToGitignore()

        if os.path.exists(self.datafile):
            self.readDatafile(self.datafile)
            self.save()
        elif os.path.exists(self.datafile_enc):
            self.decryptSecrets()


    def __getitem__(self, key):
        return self.secrets[key]

    def __setitem__(self, key, value):
        self.secrets[key] = value
        self.save()

    def __repr__(self):
        return self.secrets.__repr__()

    def save(self):
        self.saveSecrets()
        self.encryptSecrets()


    def readDatafile(self, datafile: str) -> None:
        with open(resolvePath(datafile), 'r') as f:
            self.secrets = yaml.load(f, Loader=yaml.FullLoader)

    def saveSecrets(self) -> None:
        with open(resolvePath(self.datafile), 'w') as f:
            yaml.dump(self.secrets, f)

    def addToGitignore(self) -> None:
        with open(".gitignore", "a+") as f:
            f.seek(0)
            for line in f:
                if self.path == line.strip("\n"):
                    break
            else:
                f.write(self.datafile + '\n')

    def setPublicKey(self):
        if not self.public_key:
            if self.public_key_file and self.gh_user:
                raise Exception('only one public key may be provided')

            if self.gh_user:
                with urllib.request.urlopen(f'https://github.com/{self.gh_user}.keys') as response:
                    self.public_key = RSA.importKey(response.readline()) #.decode('utf8').strip()
            else:
                with open(self.public_key_file, 'rb') as f:
                    self.public_key = RSA.importKey(f.readline())

    def getPublicKey(self) -> str:
        if not self.public_key:
            self.setPublicKey()

        return self.public_key

    def getPrivateKey(self) -> str:
        if not self.private_key:
            with open(resolvePath(self.private_key_file), 'r') as f:
                self.private_key = RSA.importKey(f.read())
        return self.private_key

    def decryptSecrets(self) -> None:
        self.decryptFile(self.datafile_enc)

    def encryptSecrets(self) -> None:
        self.encryptData(yaml.dump(self.secrets).encode('utf-8'))

    def decryptFile(self, datafile_enc: str) -> None:

        private_key = self.getPrivateKey()

        with open(resolvePath(datafile_enc), 'rb') as f:
            # pull bytes off top of file
            enc_session_key, nonce, tag, ciphertext = \
            [ f.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

        # Decrypt the session key with the private RSA key
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)

        # Decrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)

        self.secrets = yaml.load(data.decode("utf-8"), Loader=yaml.FullLoader)

    def encryptData(self, data : str) -> None:
        public_key = self.getPublicKey()
        session_key = get_random_bytes(16)

        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(public_key)
        enc_session_key = cipher_rsa.encrypt(session_key)

        # Encrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)
        with open(resolvePath(self.datafile_enc), 'wb') as f:
            [f.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
