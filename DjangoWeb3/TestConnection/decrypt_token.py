from datetime import timezone, datetime

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import json
from cryptography.hazmat.primitives import serialization
import base64
from django.conf import settings
from .loger_config import setup_logger
from .models import TransactionId

logger = setup_logger(__name__)


def load_public_key(filename):
    with open(filename, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
        )
    return public_key


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
        logger.info("Token is valid")
        return True
    except Exception as e:
        logger.warn("Invalid token")
        return False


def check_transaction_id(transaction_id):
    if TransactionId.objects.filter(transaction_id=transaction_id).exists():
        logger.info("Transaction ID already exists")
        return False
    try:
        new_transaction_id = TransactionId(transaction_id=transaction_id)
        new_transaction_id.save()
    except Exception:
        return False
    return True


def check_timestamp_token(expire_token):
    logger.debug(f"date token: {expire_token}")
    logger.debug(f" date instant: {datetime.utcnow().isoformat()}")
    if expire_token < datetime.utcnow().isoformat():
        logger.info("Token expired")
        return False
    return True


def decrypt_routine(request):
    auth_header = request.headers.get('Authorization')
    transaction_id = request.headers.get('TransactionId')
    timestamp = request.headers.get('Expires')
    public_key = load_public_key("./public_key_DjangoWeb3.pem")
    logger.debug(f"{auth_header}")
    logger.debug(f"{transaction_id}")
    logger.debug(f"{timestamp}")
    if not auth_header or not transaction_id or not timestamp:
        return False
    if not decrypt(request.data, auth_header, public_key):
        return False
    if not check_timestamp_token(timestamp):
        return False
    if not check_transaction_id(transaction_id):
        return False
    return True

