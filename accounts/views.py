from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from accounts.forms import UserLoginForm, UserRegistForm, UserAddressForm
from accounts.models import User, UserAddress
from utils import constants
from utils.verify import VerifyCode


def user_login(request):
    """用户登录"""
    # 如果登录是从其他页面跳转过来的，会带next参数，如果有next参数，登录完成后，需要跳转到
    # next所对应的地址，否则，跳转到首页上去
    # 一开始访问的时候就定义好这个地址
    next_url = request.GET.get('next', 'index')
    # 第一次访问URL，GET请求，展示表单，供用户输入
    # 第二次访问URL，POST请求
    if request.method == 'POST':
        # 实例化UserLoginForm对象时，需要传request参数，
        # 原来实例化UserLoginForm对象
        # form = UserLoginForm(request.POST),request.POST其实是data
        form = UserLoginForm(request=request, data=request.POST)
        print(request.POST)
        client = VerifyCode(request)
        code = request.POST.get('vcode', None)
        print(code)
        rest = client.validate_code(code)
        print('验证结果：', rest)
        # 表单是否通过了验证
        if form.is_valid():
            # 执行登录
            # 这个是form的验证后返回的数据
            data = form.cleaned_data

            # 使用自定义的方式实现登录
            # 查询用户信息，form验证后的数据提取username和password
            # 在数据库中取出这个用户
            # user = User.objects.get(username=data['username'], password=data['password'])
            # 设置用户ID保存到session
            # request.session['user_id'] = user.id
            # 登录后的跳转，跳转到首页
            # return redirect('index')

            # 使用django-auth来实现登录，这些都是django-auth提供的登录的方法更简单
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                # login
                login(request, user)
                request.session['user_id'] = user.id
                # 登录后的跳转
                # 在开头定义这个next_url并且有解释
                return redirect(next_url)
        else:
            # 打印异常
            print(form.errors)
    else:
        form = UserLoginForm(request)
    return render(request, 'login.html', {
        'form': form,
        # 把next_url带到模板中
        'next_url': next_url
    })


def user_logout(request):
    """用户退出登录"""
    logout(request)
    return redirect('index')


def user_register(request):
    """用户注册"""
    if request.method == 'POST':
        # 因为
        form = UserRegistForm(request=request, data=request.POST)
        if form.is_valid():
            # 调用注册方法
            form.register()
            return redirect('index')
            # return HttpResponse('ok')
        else:
            print(form.errors)
    else:
        form = UserRegistForm(request=request)
    return render(request, 'register.html', {
        'form': form
    })


# 表示用户在没有登录的时候是不能访问相应的网址的
@login_required
def address_list(request):
    """地址列表"""
    my_addr_list = UserAddress.objects.filter(user=request.user, is_valid=True)
    return render(request, 'address_list.html', {
        'my_addr_list': my_addr_list
    })


@login_required
def address_edit(request, pk):
    """地址新增或者编辑"""
    # 用request.user取到user，传给form表单类的实例对象
    user = request.user
    addr = None
    # 前端代码中所在地区为什么没有显示，是因为赋值，在form表单上自己定义的地址，可以
    # 初始化的进行赋值
    initial = {}
    # 如果pk是数字，则表示修改
    if pk.isdigit():
        # 查询相关的地址信息
        addr = get_object_or_404(UserAddress, pk=pk, user=user, is_valid=True)
        # 得到省市区赋值给初始化的地址，这个get_regin_format是在view中写好的
        initial['region'] = addr.get_regin_format()
    if request.method == 'POST':
        form = UserAddressForm(request=request, data=request.POST,
                               # 之前是只在get第一次请求的时候加上了下面这两个参数，但是保存的
                               # 时候是新增了一个地址，加上这两个参数后就是修改原来的地址了
                               instance=addr, initial=initial)
        if form.is_valid():
            form.save()
            return redirect('accounts:address_list')
    else:
        # 在是get请求的时候把这个地址传过去，因为post是需要提交表单的，get就是第一次请求的时候有
        # 一个默认地址，这样不会有省市区的默认值，加上initial=initial就有了
        # instance=addr传递到form中
        form = UserAddressForm(request=request, instance=addr, initial=initial)
    return render(request, 'address_edit.html', {
        'form': form
    })


# pk是要删除地址的主键
def address_delete(request, pk):
    """删除地址"""
    addr = get_object_or_404(UserAddress, pk=pk, is_valid=True, user=request.user)
    addr.is_valid = False
    addr.save()
    return HttpResponse('ok')
