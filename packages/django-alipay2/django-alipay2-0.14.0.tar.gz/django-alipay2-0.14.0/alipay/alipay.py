# coding: utf-8
# https://doc.open.alipay.com/doc2/detail.htm?spm=a219a.7629140.0.0.FV5dWW&treeId=62&articleId=103740&docType=1

import logging
from hashlib import md5
from urllib.parse import urlencode
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA1
import base64

ALIPAY_GATEWAY = 'https://mapi.alipay.com/gateway.do?'
ALIPAY_INPUT_CHARSET = "utf-8"
ALIPAY_SIGN_TYPE_MD5 = "MD5"
ALIPAY_SIGN_TYPE_RSA = "RSA"

GOODS_TYPE_VIRTUAL = 0
GOODS_TYPE_PHYSICAL = 1

log = logging.getLogger('alipay')


def encode_value(v):
    if isinstance(v, str):
        return v
    elif isinstance(v, int):
        return str(v)
    elif isinstance(v, float):
        return '{}'.format(round(v, 2))
    elif isinstance(v, list):
        return '^'.join([encode_value(x) for x in v])
    else:
        raise Exception("can't encode value: %s" % v)


def _build_sign_body(params):
    fields = [k for k, v in params.items()
              if k not in ('sign', 'sign_type') and v is not None]
    fields.sort()

    s = '&'.join(['{}={}'.format(k, encode_value(params[k])) for k in fields])
    return s


def create_sign(params, key, encoding=ALIPAY_INPUT_CHARSET, sign_type=ALIPAY_SIGN_TYPE_MD5):
    assert sign_type in (ALIPAY_SIGN_TYPE_MD5, ALIPAY_SIGN_TYPE_RSA)

    s = _build_sign_body(params)
    if sign_type is ALIPAY_SIGN_TYPE_RSA:
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA1.new(s.encode(encoding)))
        return base64.encodebytes(signature).decode().replace("\n", "")

    else:
        s = s + key
        return md5(s.encode(encoding)).hexdigest()


class Result(object):
    def __init__(self):
        # 关键参数 =============================================
        self.sign_type = None
        self.sign = None
        self.out_trade_no = None
        self.trade_no = None
        self.trade_status = None
        self.seller_email = None
        self.buyer_email = None
        self.total_fee = None

        # 以下为非关键参数 ======================================
        self.notify_time = None
        self.notify_id = None
        self.notify_type = None
        self.subject = None
        self.payment_type = '1'
        self.seller_id = None
        self.buyer_id = None
        self.body = None
        self.extra_common_param = None

        # return only
        self.is_success = None  # T/F, 表示接口调用是否成功，并不表明业务处理结果。
        self.exterface = None  # String, 标志调用哪个接口返回的链接。

        # notify only
        self.gmt_create = None
        self.gmt_payment = None
        self.gmt_close = None
        self.refund_status = None
        self.gmt_refund = None
        self.price = None
        self.quantity = None
        self.discount = None
        self.is_total_fee_adjust = None
        self.use_coupon = None
        self.business_scene = None


class AlipayClient(object):
    SERVICE_DIRECT = 'create_direct_pay_by_user'
    SERVICE_WAP = 'alipay.wap.create.direct.pay.by.user'

    def __init__(self, pid, key, seller_email,
                 goods_type=GOODS_TYPE_VIRTUAL,
                 input_charset=ALIPAY_INPUT_CHARSET,
                 sign_type=ALIPAY_SIGN_TYPE_MD5,
                 gateway=ALIPAY_GATEWAY,
                 rsa_public_raw_key='',
                 **defaults):
        self._raw_key = key

        self.partner = pid
        self.seller_email = seller_email
        self._input_charset = input_charset
        self.sign_type = sign_type
        self.gateway = gateway
        self.payment_type = 1

        self.defaults = defaults
        self.defaults["goods_type"] = goods_type

        if sign_type is ALIPAY_SIGN_TYPE_RSA:
            assert rsa_public_raw_key, 'rsa_public_raw_key is required'
            self.sign_key = RSA.importKey(key)
            self.rsa_public_key = RSA.importKey(rsa_public_raw_key)
        else:
            self.sign_key = key

    def _create_pay_url(self, service, out_trade_no, subject, body, total_fee, notify_url, return_url,
                        show_url=None, expire='15m', **kwargs):
        params = self.defaults.copy()

        if service == self.SERVICE_DIRECT:
            params['seller_email'] = self.seller_email
        elif service == self.SERVICE_WAP:
            params['seller_id'] = self.partner

        params.update({
            'service': service,
            'partner': self.partner,
            '_input_charset': self._input_charset,
            'sign_type': self.sign_type,
            'out_trade_no': out_trade_no,
            'subject': subject,
            'body': body,
            'payment_type': self.payment_type,
            'total_fee': total_fee,
        })

        kwargs.update({
            'notify_url': notify_url,
            'return_url': return_url,
            'show_url': show_url,
            'it_b_pay': expire,
        })
        for k, v in kwargs.items():
            if v is not None:
                params[k] = v

        params = {k: v for k, v in params.items() if v is not None}

        params['sign'] = create_sign(params, self.sign_key, self._input_charset, self.sign_type)

        return self.gateway + urlencode(params)

    def create_direct_pay_url(self, out_trade_no, subject, body, total_fee, notify_url, return_url,
                              show_url=None, expire='15m', **kwargs):
        return self._create_pay_url(self.SERVICE_DIRECT, out_trade_no, subject, body, total_fee, notify_url, return_url,
                                    show_url, expire, **kwargs)

    # reference: https://docs.open.alipay.com/60/104790/
    def create_wap_pay_url(self, out_trade_no, subject, body, total_fee, notify_url, return_url,
                           show_url=None, expire='15m', **kwargs):
        return self._create_pay_url(self.SERVICE_WAP, out_trade_no, subject, body, total_fee, notify_url, return_url,
                                    show_url, expire, **kwargs)

    def get_verified_result(self, arguments):
        assert isinstance(arguments, dict)
        assert arguments['sign_type'] == self.sign_type

        if self.sign_type is ALIPAY_SIGN_TYPE_RSA:
            raw_content = _build_sign_body(arguments)
            key = self.rsa_public_key
            digest = SHA1.new()
            digest.update(raw_content.encode(ALIPAY_INPUT_CHARSET))

            signer = PKCS1_v1_5.new(key)
            assert bool(signer.verify(digest, base64.decodebytes(arguments['sign'].encode())))
        else:
            sign = create_sign(arguments, self.sign_key, ALIPAY_INPUT_CHARSET, arguments['sign_type'])
            assert sign == arguments['sign']

        result = Result()
        for k, v in arguments.items():
            setattr(result, k, v)
        return result


if __name__ == '__main__':
    pass
