import base64
import json
from datetime import datetime, timedelta

from amqp import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import serialization
from .UniqId import Uniqid


class Signature:
    def __init__(self):
        pass

    @staticmethod
    def save_private_key(private_key, filename):
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(filename, 'wb') as f:
            f.write(pem)

    @staticmethod
    def generate_keys():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        return private_key

    @staticmethod
    def getPublicKey():
        with open("private_key.pem", "rb") as f:
            private_key = load_pem_private_key(f.read(), None)

        public_key = private_key.public_key()

        pem_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return pem_public_key

    @staticmethod
    def getPrivateKey(path):
        f = open(path, "rb")
        load_key = load_pem_private_key(f.read(), None)
        return load_key

    @staticmethod
    def create_signed_token(data, path):

        private_key = Signature.getPrivateKey(path)
        data_json = json.dumps(data)

        data_bytes = data_json.encode('utf-8')
        signature = private_key.sign(
            data_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        signature_encoded = base64.b64encode(signature).decode('utf-8')
        headers = {"Authorization": str(signature_encoded),
                   "TransactionId": str(Uniqid.generate()),
                   "Expires": (datetime.utcnow() + timedelta(minutes=10)).isoformat()}
        print("[API] data", data)
        print("[API] signature_encoded", signature_encoded)
        print("[API] headers", headers)
        return data, signature_encoded, headers
