from django.shortcuts import render, HttpResponse
import random
from utils.tencent.sms import send_sms_single
from django.conf import settings
# Create your views here.


def send_sms(request):
    """ 发送短信
        ?tpl=login  -> 614333
        ?tpl=register -> 614334
        ?tp;=reset_password'->614332
    """

    # 用户请求过来判断是哪种短信服务
    tpl = request.GET.get('tpl')

    # 根据短信服务类型从设置中获得服务ID
    template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
    if not template_id:
        return HttpResponse('模板不存在')

    # 产生随机验证码
    code = random.randrange(1000, 9999)

    # 根据服务类型发送短信
    res = send_sms_single('13875769471', template_id, [code, ])

    # 如果res的返回值中的result等于0，表示短信发送成功，否则失败
    if res['result'] == 0:
        return HttpResponse('成功')
    else:
        return HttpResponse(res['errmsg'])
