from django.db.models import Sum

from utils import constants


def shop_cart(request):
    """当前用户的购物车信息"""
    # 当前用户
    user = request.user
    # 购物车信息，商品列表
    cart_list = []
    # 这些商品值多少钱
    cart_total = None
    # 商品的个数
    cart_count = 0
    # 有可能用户没有登录，如果用户登录了
    if user.is_authenticated:
        # 我的购物车商品列表
        cart_list = user.carts.filter(
            status=constants.ORDER_STATUS_INIT
        )
        # amount总额，count购买的总数量
        cart_total = cart_list.aggregate(sum_amount=Sum('amount'),
                                         sum_count=Sum('count'))
        cart_count = cart_list.count()
    return {
        'cart_count': cart_count,  # 购物车中的商品数量
        'cart_list': cart_list,
        'cart_total': cart_total
    }