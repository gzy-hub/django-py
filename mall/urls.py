from django.conf.urls import url

from mall import views

urlpatterns = [
    # 商品列表 def function实现
    # url(r'^prod/list/$', views.product_list, name='product_list'),
    # 使用class来实现
    url(r'^prod/list/$', views.ProductList.as_view(), name='product_list'),
    # 加载html片段的地址
    url(r'^prod/load/list/$', views.ProductList.as_view(
        # 使得可以复用ProductList里面的搜索和分页的功能
        template_name='product_load_list.html'
    ), name='product_load_list'),
    # 商品详情，\s表示匹配任何空字符，\S表示匹配任何字符
    url(r'^prod/detail/(?P<pk>\S+)/$', views.product_detail, name='product_detail'),
    # 商品分类
    url(r'^prod/classify/$', views.prod_classify, name='prod_classify'),
]