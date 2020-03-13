from django.http import HttpResponse


from accounts.models import User


# 需要传一些参数，这些参数就是一个函数get_response
def ip_middleware(get_response):

    def middleware(request):

        # 请求到达前的业务逻辑
        print('请求到达前的业务逻辑')
        # 请求不满足业务规则：IP被限制
        # 得到用户请求的IP地址
        ip = request.META.get('REMOTE_ADDR', None)
        ip_disable_list = [
            '127.0.0.1'
        ]
        print(ip)
        # for ip_dis in ip_disable_list:
        #     if ip_dis == ip:
        if ip in ip_disable_list:
            return HttpResponse('not allowd', status=403)
        # reponse在get_response得到
        reponse = get_response(request)

        # 在视图函数调用之后的业务逻辑
        print('在视图函数调用之后的业务逻辑')
        return reponse

    return middleware


# 没有使用django-auth是先输入用户名和密码，登录，把用户ID存在一个session中，其他用到的在
# session中取出来用。用了django-auth后，直接用request.user就行。
class MallAuthMiddleware(object):
    """自定义的登录验证中间件"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request,  *args, **kwargs):
        print('MallAuthMiddleware请求到达前的业务逻辑')

        # 在用户accounts的模块view视图中，要把request.session['user_id'] = user.id传到session中
        # 在session中取到这个用户
        user_id = request.session.get('user_id', None)
        if user_id:
            user = User.objects.get(pk=user_id)
        else:
            user = None
        # 查到user设置到request中去
        request.my_user = user
        reponse = self.get_response(request)

        # 在视图函数调用之后的业务逻辑
        print('MallAuthMiddleware在视图函数调用之后的业务逻辑')
        return reponse
