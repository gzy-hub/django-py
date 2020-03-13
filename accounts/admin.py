from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from accounts.models import User, UserProfile, UserAddress


# 这部分代码的作用就是为了修饰该模块在后台管理的显示效果。
# @admin.register()作用是为了让User可以在后台显示，需要在admin后台进行注册。
@admin.register(User)
class UserAdmin(UserAdmin):
    """用户基础信息管理"""
    """
    由于自定义的User模型继承了Django的用户模型（AbstractUser），
    因此可以使用UserAdmin这个后台用户展示模型的类。继承这个类后，可以在这个显示模型的
    基础上进行重新定义。
    """
    # fields = ('integral', 'level', 'nickname')
    list_display = ['format_username', 'nickname', 'integral', 'is_active']
    # 支持按用户名、昵称进行搜索
    search_fields = ('username', 'nickname')
    # 添加自定义的方法，配置到admin显示
    actions = ['disable_user', 'enable_user']
    # 这个是直接在UserAdmin这个父类中复制出来的
    # 这个地方是点击用户，进去之后用户的一些信息
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        # 在admin的后台中，用户这里是一块一块都显示的如Personal info是标题，后面是这个标题
        # 下面的一系列的表单
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email',
                                        'integral', 'nickname')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # 传一个对象obj过来，对象就是每一行的用户对象
    def format_username(self, obj):
        """用户名脱敏处理"""
        return obj.username[0:3] + '***'
    # 修改前台页面的列名显示
    format_username.short_description = '用户名'

    # 为了自己的一些需求需要自定义一些方法，在admin那里能用到
    # 写自定义方法时：需要传request, queryset两个参数
    def disable_user(self, request, queryset):
        """批量禁用选中的用户"""
        queryset.update(is_active=False)
    disable_user.short_description = '批量禁用用户'

    def enable_user(self, request, queryset):
        """批量禁用选中的用户"""
        queryset.update(is_active=True)
    enable_user.short_description = '批量启用用户'

# admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """用户详细信息"""
    list_display = ('user', 'phone_no', 'sex')


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    """用户地址管理"""
    list_display = ('user', 'province', 'city',
                    'username', 'address', 'phone',
                    'is_valid', 'is_default')
    search_fields = ('user__username', 'user__nickname',
                     'phone', 'username')