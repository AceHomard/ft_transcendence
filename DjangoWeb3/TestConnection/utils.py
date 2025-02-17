from .serializers import Matchserializer, Tournament_group_data, SendDbMatchToSerializer
from .StoreInDB import get_tx_from_db
from operator import itemgetter

def Serialize_and_validate_data(data):
    match_json = SendDbMatchToSerializer(data)
    if match_json.is_valid():
        return match_json.data
    return None


def process_matches(matchs_from_BC, matchs_from_DB):
    return_matches = []
    if matchs_from_BC is not None:
        for match in matchs_from_BC:
            match_data = Serialize_and_validate_data(match)
            if match_data:
                match_data['from_blockchain'] = True
                match_data['tx_hash'] = get_tx_from_db(match_data)
                return_matches.append(match_data)
    return_matches.extend(matchs_from_DB or [])
    return_matches.sort(key=itemgetter('timestamp'), reverse=True)
    return return_matches


class TransactionToLongError(Exception):
    def __init__(self, txn_hash):
        self.txn_hash = txn_hash


class FailedTransactionError(Exception):
    pass
