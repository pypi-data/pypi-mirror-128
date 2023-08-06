from django.conf import settings
from django.utils.module_loading import import_string

from alipay.alipay import AlipayClient

DEFAULT_GATEWAY = 'https://mapi.alipay.com/gateway.do?'


def get_alipay_api(seller_email=None) -> 'AlipayAPI':
    api_provider_name = settings.ALIPAY.get('api_provider')
    if api_provider_name:
        api_provider = import_string(api_provider_name)
        return api_provider(seller_email)

    else:
        assert not seller_email or seller_email == settings.ALIPAY['seller_email'], 'seller_email和settings不匹配'

        return AlipayAPI(
            pid=settings.ALIPAY['pid'],
            key=settings.ALIPAY['key'],
            seller_email=settings.ALIPAY['seller_email'],
            gateway=settings.ALIPAY.get('gateway'),
            sign_type=settings.ALIPAY.get('sign_type'),
            rsa_public_raw_key=settings.ALIPAY.get('rsa_public_raw_key'),
        )


class AlipayAPI:
    def __init__(self, pid, key, seller_email, gateway=None, sign_type=None, rsa_public_raw_key=None):
        self.seller_email = seller_email
        self.pid = pid
        self.key = key
        self.gateway = gateway or DEFAULT_GATEWAY
        self.sign_type = sign_type
        self.rsa_public_raw_key = rsa_public_raw_key

    @property
    def client(self):
        return AlipayClient(self.pid, self.key, self.seller_email, gateway=self.gateway,
                            sign_type=self.sign_type,
                            rsa_public_raw_key=self.rsa_public_raw_key)
