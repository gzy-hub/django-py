import re

from django import forms
from django.contrib.auth import authenticate, login

from accounts.models import User, UserAddress
from utils.verify import VerifyCode


class UserLoginForm(forms.Form):
    """用户登录表单"""
    username = forms.CharField(label='用户名', max_length=64)
    password = forms.CharField(label='密码', max_length=64,
                               widget=forms.PasswordInput,
                               # 在页面上报错是英文的，不友好，修改一下
                               error_messages={
                                   'required': '请输入密码'
                               })
    verify_code = forms.CharField(label='验证码', max_length=4,
                                  error_messages={
                                      'required': '请输入验证码'
                                  })

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    # def clean_username(self):
    #     """验证用户名 hook 钩子函数"""
    #     username = self.cleaned_data['username']
    #     print(username)
    #     # 判断用户名是否为手机号
    #     pattern = r'^0{0,1}1[0-9]{10}$'
    #     if not re.search(pattern, username):
    #         raise forms.ValidationError('请输入正确的手机号码')
    #     return username

    def clean_verify_code(self):
        """验证用户输入的验证码是否正确"""
        # cleaned_data返回验证后的表单数据
        verify_code = self.cleaned_data['verify_code']
        if not verify_code:
            raise forms.ValidationError('请输入验证码')
        # 这里需要传一个request，那就直接在上面重写一下__init__构造函数，把request传进来
        # 那么在实例化form对象时需要传request
        client = VerifyCode(self.request)
        if not client.validate_code(verify_code):
            raise forms.ValidationError('您输入的验证码不正确')
        return verify_code

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        # 获取用户名和密码，不建议使用[]的方式
        # username = cleaned_data['username']

        username = cleaned_data.get('username', None)
        password = cleaned_data.get('password', None)
        if username and password:
            # 查询用户名和密码匹配的用户
            user_list = User.objects.filter(username=username)
            if user_list.count() == 0:
                raise forms.ValidationError('用户名不存在')
            # # 验证密码是否正确
            # if not user_list.filter(password=password).exists():
            #     raise forms.ValidationError('密码错误')
            # authenticate需要传三个参数request和姓名和密码，第一个参数可以不传
            if not authenticate(username=username, password=password):
                raise forms.ValidationError('密码错误')
        return cleaned_data


class UserRegistForm(forms.Form):
    """用户注册表单"""
    username = forms.CharField(label='用户名', max_length=64)
    nickname = forms.CharField(label='昵称', max_length=64)
    password = forms.CharField(label='密码', max_length=64, widget=forms.PasswordInput)
    password_repeat = forms.CharField(label='重复密码', max_length=64, widget=forms.PasswordInput)
    verify_code = forms.CharField(label='验证码', max_length=4)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_username(self):
        """验证用户名是否已经被注册"""
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('用户名已存在')
        return data

    def clean_verify_code(self):
        """验证用户输入的验证码是否正确"""
        verify_code = self.cleaned_data['verify_code']
        if not verify_code:
            raise forms.ValidationError('请输入验证码')
        client = VerifyCode(self.request)
        # if只有true的时候才会执行下面的情况if True就是if not False
        # 也就是说client.validate_code(verify_code)是False时
        # 当验证码不正确时，返回False。
        if not client.validate_code(verify_code):
            raise forms.ValidationError('您输入的验证码不正确')
        return verify_code

    def clean(self):
        cleaned_date = super().clean()
        password = cleaned_date.get('password', None)
        password_repeat = cleaned_date.get('password_repeat', None)
        if password and password_repeat:
            if password != password_repeat:
                raise forms.ValidationError('两次输入密码不一致')
        return cleaned_date

    def register(self):
        """注册方法"""
        data = self.cleaned_data
        # 1.创建用户
        User.objects.create_user(username=data['username'],
                                 password=data['password'],
                                 nickname='昵称',
                                 level=0)
        # 2.自动登录
        user = authenticate(username=data['username'],
                            password=data['password'])
        login(self.request, user)
        return user


class UserAddressForm(forms.ModelForm):
    """"地址新增|修改表单"""

    # 省市区处理的基本思路：
    # 前端传递的省市区参数为数组形式------后台手动修改关于数组形式的字段拆解-----
    # 拆解完成后与model 中定义的字段进行对应-------修改form 表单中对应的数据验证方式。
    region = forms.CharField(label='大区域选项', max_length=64, required=True,
                             error_messages={
                                 'required': '请选择地址'
                             })

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    class Meta:
        model = UserAddress
        fields = ['address', 'username', 'phone', 'is_default']
        # 设置默认地址时，定制界面的显示，定制就用widgets
        widgets = {
            'is_default': forms.CheckboxInput(attrs={
                # 不加这些属性，前台是有一个勾选的框，怎么能点击设置默认地址的呢，就是把class
                # 属性设置的和以前那个点击的一样
                'class': 'weui-switch'
            })
        }

    def clean_phone(self):
        """验证用户输入的手机号码"""
        phone = self.cleaned_data['phone']
        # 判断用户名是否为手机号
        pattern = r'^0{0,1}1[0-9]{10}$'
        if not re.search(pattern, phone):
            raise forms.ValidationError('请输入正确的手机号码')
        return phone

    def clean(self):
        cleaned_data = super().clean()
        # 查询当前登录用户的地址数据
        # 因为用了django自带的用户系统，用户可以直接用request.user取到，所以要在表单类中写一个
        # 构造函数接收request，在视图函数中实例化表单对象时，接收这个request
        addr_list = UserAddress.objects.filter(is_valid=True, user=self.request.user)
        if addr_list.count() >= 20:
            raise forms.ValidationError('最多只能添加20个地址')
        return cleaned_data

    # 保存方法需要重写一下，因为省市区重新写到region中了
    def save(self, commit=True):
        obj = super().save(commit=False)
        # 在前台页面穿过来的form的内容
        region = self.cleaned_data['region']
        # 省市区的数据
        (province, city, area) = region.split(' ')
        obj.province = province
        obj.city = city
        obj.area = area
        obj.user = self.request.user

        # 修改的时候，如果已经有了默认地址，当前页勾选了默认地址选项
        # 需要把之前的地址都改为非默认的地址
        if self.cleaned_data['is_default']:
            # update是orm中更新
            UserAddress.objects.filter(is_valid=True, user=self.request.user,
                                       is_default=True).update(is_default=False)

        obj.save()

