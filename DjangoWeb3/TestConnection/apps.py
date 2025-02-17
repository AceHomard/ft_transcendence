from django.apps import AppConfig
from django.conf import settings
from .ConnectionToBC import StoreScore


class Web3Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TestConnection'

    def ready(self):
        super().ready()
        if not hasattr(settings, 'STORE_SCORE'):
            settings.STORE_SCORE = StoreScore(settings.INFURA_URL, settings.CONTRACT_ADDRESS, settings.ABI, settings.ETH_ADDRESS, settings.META_PK)
#