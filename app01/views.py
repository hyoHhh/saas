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


from django import forms
from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class RegisterModelForm(forms.ModelForm):

    # 重写字段

    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])

    # 如果model中有就覆盖
    password = forms.CharField(
        label='密码',
        # 插件
        widget=forms.PasswordInput())

    # 如果没有就新增，但是model中不新增
    confirm_password = forms.CharField(
        label='重复密码',
        widget=forms.PasswordInput())

    #
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput())

    class Meta:
        model = models.UserInfo

        # 页面展示顺序
        fields = ['username', 'email', 'password', 'confirm_password', 'mobile_phone', 'code']



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 给每一个modelform添加属性并且设置默认值

        # self.fields 所有字段
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)


def register(request):

    form =RegisterModelForm()
    return render(request,"app01/register.html",{"form":form})

