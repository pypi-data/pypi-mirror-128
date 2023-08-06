"""
原则上需要定义两个view name：
    - alipay_redirect
    - alipay_callback

Example urlpatterns
-------------------

urlpatterns = [
        url('^redirect/(?P<pk>.*?)/$', AlipayRedirectView.as_view(), name='alipay_redirect'),
        url('^callback/$', AlipayCallbackView.as_view(), name='alipay_callback'),
    ]
"""

import user_agents
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from alipay.helpers import get_alipay_api
from alipay.models import AlipayPayment


class AlipayRedirectView(View):
    """
    他人生成AlipayPayment以后，跳转到本view就能重定向到alipay，继续完成支付流程
    样例见： example_alipay_create_view
    """
    UA_WEB = 'web'  # web直接到账
    UA_WAP = 'wap'  # 手机支付
    UA_AUTO = 'auto'  # 根据UA来决定用WAP还是WEB

    def handle_redirect(self, redirect_url):
        """ 得到alipay支付地址以后，定义如何跳转（默认为直接跳转，可以自己改成打开loading页面，用JS跳转 """
        return redirect(redirect_url)

    @classmethod
    def get_callback_url(cls, request, payment, is_notify=False):
        return request.build_absolute_uri(reverse('alipay_callback'))

    def get(self, request, out_no):
        ua_mode = request.GET.get('ua', self.UA_WEB)  # 默认用web模式，因为WAP的需要另外申请，不自动开通

        payment = get_object_or_404(AlipayPayment, out_no=out_no)
        alipay_api = get_alipay_api(payment.seller_email)
        if not payment.seller_email:
            payment.seller_email = alipay_api.seller_email
            payment.save()

        if ua_mode == self.UA_AUTO:
            ua = user_agents.parse(request.META['HTTP_USER_AGENT'])
            if ua.is_pc:
                ua_mode = self.UA_WEB
            else:
                ua_mode = self.UA_WAP

        assert ua_mode in [self.UA_WEB, self.UA_WAP]
        if ua_mode == self.UA_WEB:
            create_pay_url = alipay_api.client.create_direct_pay_url
        else:
            create_pay_url = alipay_api.client.create_wap_pay_url

        pay_url = create_pay_url(
            payment.out_no,
            payment.subject,
            payment.body,
            "{:.2f}".format(payment.amount_total),
            notify_url=self.get_callback_url(request, payment, is_notify=True),
            return_url=self.get_callback_url(request, payment, is_notify=False),
            expire=payment.expire,
        )
        return self.handle_redirect(pay_url)


@method_decorator(csrf_exempt, name='dispatch')
class AlipayCallbackView(View):
    """
    从alipay支付成功以后，回来的页面，
    页面自己会处理payment成功的逻辑，成功以后会发送 payment_succeed signal
    业务逻辑只需要connect payment_succeed，然后做相应的处理即可
    """

    template_name = 'alipay/return.html'

    def payment_succeed(self, payment):
        """ 支付成功以后的返回结果，按需定义 """
        return render(self.request, self.template_name, context=dict(payment=payment))

    def payment_failed(self, payment, errors):
        """ 执行支付失败后的返回结果，按需定义 """
        print("handle_payment_execute_error", payment, errors)
        return HttpResponseServerError()

    def get(self, request):
        payment = self.handle_alipay_callback(request.GET)
        if payment:
            return self.payment_succeed(payment)
        else:
            return HttpResponse('error')

    def post(self, request):
        if self.handle_alipay_callback(request.POST):
            return HttpResponse("success")
        else:
            return HttpResponse("failed")

    @classmethod
    def handle_alipay_callback(cls, data):
        result = None
        try:
            seller_email = data['seller_email']
            alipay_api = get_alipay_api(seller_email)
            result = alipay_api.client.get_verified_result(data)
            assert result.is_success != 'F', 'payment failed'

            payment = AlipayPayment.objects.get(out_no=result.out_trade_no)

            # status 有推进才会接着处理
            if payment.status_weight(result.trade_status) > payment.status_weight(payment.status):
                payment.buyer_email = result.buyer_email
                payment.buyer_id = result.buyer_id
                payment.no = result.trade_no
                payment.status = result.trade_status
                payment.save()
            return payment

        except Exception as e:
            print("trade failed error={} data={} result={}".format(e, data, result))
            return None
