from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http import HttpResponse
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView

from mall.models import Product
from mine.models import Order, Cart
from utils import constants, tools


@login_required
def index(request):
    """个人中心首页"""
    return render(request, 'mine.html', {
        'constants': constants
    })


# DetailView用于显示一个特定类型对象的详细信息。
# 根据具体需要继承相应的视图
class OrderDetailView(DetailView):
    """订单详情"""
    model = Order
    # 要根据模型的sn字段进行查询
    slug_field = 'sn'
    # 从url获取条件pk的别名是sn
    slug_url_kwarg = 'sn'
    template_name = 'order_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['constants'] = constants
        return context


# 购物车在个人中心这边，在商品详情点击加入购物车发送一个POST请求，
# 选择购买数量，调用个人中心这边加入购物车的函数
@login_required
# 修改了多张表，开启一个事务
@transaction.atomic()
# 需要传一个商品的ID，点击添加到购物车，不需要添加的页面
def cart_add(request, prod_uid):
    """添加商品到购物车"""
    user = request.user
    # 要得到商品的信息
    product = get_object_or_404(Product, uid=prod_uid,
                                is_valid=True,
                                status=constants.PRODUCT_STATUS_SELL)

    # 购买数量
    count = int(request.POST.get('count', 1))
    # 校验库存
    if product.ramain_count < count:
        return HttpResponse('no')
    # 减库存，在mall的模型中添加这么个方法
    product.update_store_count(count)
    # 生成购物车记录
    # 如果已经添加到购物车了，就把购买数量和价格更新一下
    try:
        cart = Cart.objects.get(product=product, user=user,
                                status=constants.ORDER_STATUS_INIT)
        # 更新价格和数量
        # cart.count指的是原来有的数量，在加上现在的数量
        count = cart.count + count
        cart.count = count
        # 价格为数量乘以单价
        cart.amount = count * cart.price
        cart.save()
    except Cart.DoesNotExist:
        # 没有加入购物车
        Cart.objects.create(
            product=product,
            user=user,
            name=product.name,
            img=product.img,
            price=product.price,
            origin_price=product.origin_price,
            count=count,
            amount=count * product.price
        )
    return HttpResponse('ok')


@login_required
def cart(request):
    """我的购物车"""
    user = request.user
    # 我购物车中的商品列表，user.carts是Cart模型中的user的related_name为carts
    prod_list = user.carts.filter(status=constants.ORDER_STATUS_INIT)
    if request.method == 'POST':
        # 提交订单
        # 1.保存用户的地址快照
        default_addr = user.default_addr
        if not default_addr:
            # 消息通知
            messages.warning(request, '请选择地址信息')
            # 如果没有默认地址，跳转到另外一个页面，
            return redirect('accounts:address_list')
        # 订单总额计算
        # 聚合查询
        cart_total = prod_list.aggregate(sum_amount=Sum('amount'),
                                         sum_count=Sum('count'))
        # 创建一个订单
        order = Order.objects.create(
            user=user,
            sn=tools.gen_trans_id(),
            buy_amount=cart_total['sum_amount'],
            buy_count=cart_total['sum_count'],
            to_user=default_addr.username,
            to_area=default_addr.get_regin_format(),
            to_address=default_addr.address,
            to_phone=default_addr.phone
        )
        prod_list.update(
            # 2.修改购物车中的状态  已提交
            status=constants.ORDER_STATUS_SUBMIT,
            # 3.生成订单，关联到购物车
            # 在mine模块下的购物车模型是关联到订单的
            order=order
        )
        # 4.跳转到订单详情
        messages.success(request, '下单成功，请支付')
        return redirect('mine:order_detail', order.sn)

    return render(request, 'cart.html', {
        'prod_list': prod_list
    })


@login_required
def order_pay(request):
    """提交订单"""
    user = request.user
    if request.method == 'POST':
        # 在order_info页面提交一个隐藏的表单域，有sn信息，订单编号是保密的，不能让其他人看到
        sn = request.POST.get('sn', None)
        # 1.查询订单信息
        order = get_object_or_404(Order, sn=sn, user=user,
                                  status=constants.ORDER_STATUS_SUBMIT)
        # 2.验证钱够不够
        if order.buy_amount > user.integral:
            messages.error(request, '积分余额不足')
            return redirect('mine:order_detail', sn=sn)
        # 3.钱扣掉，ope_integral_account在accounts模块的models模型中
        user.ope_integral_account(0, order.buy_amount)
        # 4.修改订单状态
        order.status = constants.ORDER_STATUS_PAIED
        order.save()
        # 5.修改购物车关联的状态
        order.carts.all().update(status=constants.ORDER_STATUS_PAIED)
        messages.success(request, '支付成功')
    return redirect('mine:order_detail', sn=sn)


@login_required
def order_list(request):
    """我的订单列表"""
    status = request.GET.get('status', '')
    # 把前台接收的这个status转换一下，传给order_list.html
    try:
        status = int(status)
    except ValueError:
        status = ''
    return render(request, 'order_list.html', {
        'constants': constants,
        'status': status
    })


# 用类来写订单列表
class OrderListView(ListView):
    """基于类视图的订单列表"""
    model = Order
    template_name = 'order_list.html'

    def get_queryset(self):
        status = self.request.GET.get('status', '')
        # 该用户下面
        user = self.request.user
        query = Q(user=user)
        if status:
            query = query & Q(status=status)
        #  需要排除删除的订单exclude
        # print(Order.objects.filter(query).exclude(
        #     status=constants.ORDER_STATUS_DELETED
        # ))
        return Order.objects.filter(query).exclude(
            status=constants.ORDER_STATUS_DELETED
        )

    # 给视图传其他的参数，重写上下文的方法
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = self.request.GET.get('status', '')
        try:
            status = int(status)
        except ValueError:
            status = ''
        context['status'] = status
        context['constants'] = constants
        return context


@login_required
def prod_collect(request):
    """我的收藏"""
    return render(request, 'prod_collect.html')