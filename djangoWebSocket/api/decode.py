from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import json
from cryptography.hazmat.primitives import serialization
import base64
from Log.Log import Log
from api.models import TransactionId

def load_public_key(filename):
    with open(filename, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
        )
    return public_key


def check_transaction_id(transaction_id):
    if TransactionId.objects.filter(transaction_id=transaction_id).exists():
        Log.error("[API] Key", "Transaction ID already exists")
        return False
    try:
        new_transaction_id = TransactionId(transaction_id=transaction_id)
        new_transaction_id.save()
    except Exception:
        return False
    return True


def decrypt(message, signature, public_key):
    try:
        json_data = json.dumps(message)
        data_bytes = json_data.encode('utf-8')
        signature_bytes = base64.b64decode(signature)
        public_key.verify(
            signature_bytes,
            data_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        Log.info("[API] GET", "Token Valid")
        return True
    except Exception as e:
        Log.error("[API] GET", "Token Invalid")
        return False


def decrypt_routine(request):
    auth_header = request.headers.get('Authorization')
    transaction_id = request.headers.get('TransactionId')
    public_key = load_public_key("keydjangoWebSocketapi/gameengine/public_key.pem")

    if not auth_header or not transaction_id:
        return False
    if not decrypt(request.data, auth_header, public_key):
        return False
    if not check_transaction_id(transaction_id):
        return False
    return True
