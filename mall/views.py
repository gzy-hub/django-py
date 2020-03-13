from django.db.models import Q
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView

from mall.models import Product
from utils import constants


def product_list(request, template_name='product_list.html'):
    """商品列表"""
    prod_list = Product.objects.filter(
        status=constants.PRODUCT_STATUS_SELL,
        is_valid=True)
    # 按名称搜索
    name = request.GET.get('name', '')
    if name:
        # name__icontains包含这么一个名字
        prod_list = prod_list.filter(name__icontains=name)
    return render(request, template_name, {
        'prod_list': prod_list
    })


def product_detail(request, pk, template_name='product_detail.html'):
    """商品详情"""
    prod_obj = get_object_or_404(Product, uid=pk, is_valid=True)
    # 用户的默认地址
    user = request.user
    default_addr = None
    if user.is_authenticated:
        default_addr = user.default_addr
    return render(request, template_name, {
        'prod_obj': prod_obj,
        'default_addr': default_addr
    })


# 新的方法进行分页和搜索
# ListView 用于获取数据表中的所有数据，返回一个列表
class ProductList(ListView):
    """商品列表"""
    # 每页放多少条数据
    paginate_by = 6
    # 模板位置
    template_name = 'product_list.html'

    # 商品的结果集
    def get_queryset(self):
        query = Q(status=constants.PRODUCT_STATUS_SELL,
                  is_valid=True)

        # 按名称搜索
        name = self.request.GET.get('name', '')
        if name:
            # name__icontains表示name字段中包含页面传过来的name
            query = query & Q(name__icontains=name)

        # 按标签进行搜索，这个tag是在index的url传过来的
        # href="{% url 'mall:product_list' %}?tag=jxtj"
        tag = self.request.GET.get('tag', '')
        if tag:
            # 在mall下面的model模型中发现商品的tag是一个多对多的外键关联
            query = query & Q(tags__code=tag)
        # 按照分类进行搜索
        cls = self.request.GET.get('cls', '')
        if cls:
            query = query & Q(classes__code=cls)

        return Product.objects.filter(query)

    # 因为添加了ajax异步加载后，搜索商品中的name参数没有跟着过来，不能搜索商品了
    # 刷新一下页面之后，就不会在刷新页面了name参数需要传递到模板中来
    # 因为是基于类实现的，需要给传递到模板中的数据当中重新添加添加一个参数
    # 上下文
    def get_context_data(self, **kwargs):
        """添加额外的参数，添加搜索参数"""
        context = super().get_context_data(**kwargs)
        # 因为查询的时候除了name，如果加上销量和价格等，就会有很多参数
        # context['search_name'] = self.request.GET.get('name', '')
        context['search_data'] = self.request.GET.dict()
        return context


def prod_classify(request):
    """商品分类"""
    return render(request, 'prod_classify.html', {

    })

