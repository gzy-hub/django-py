from django.conf.urls import url

from accounts import views

urlpatterns = [
    # 用户登录
    url(r'^user/login/$', views.user_login, name='user_login'),
    # 用户退出
    url(r'^user/logout/$', views.user_logout, name='user_logout'),
    # 用户注册
    url(r'^user/register/$', views.user_register, name='user_register'),

    # 地址列表
    url(r'^user/address/list/$', views.address_list, name='address_list'),
    # 地址的修改和编辑
    # 分为两种情况：user/address/edit/add/新增  user/address/edit/12编辑
    # 起了个名字叫pk
    url(r'^user/address/edit/(?P<pk>\S+)/$', views.address_edit, name='address_edit'),
    #
    url(r'^user/address/delete/(?P<pk>\S+)/$', views.address_delete, name='address_delete'),

]