from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render, get_object_or_404

# Create your views here.
from system.models import News
from utils import constants
from utils.verify import VerifyCode


def news_list(request, template_name='news_list.html'):
    """新闻列表"""
    # 对内容进行分页，用python自带的
    page = request.GET.get('page', 1)
    page_size = 20  # 每页放20条数据
    # 类型为新闻的，有效的
    news = News.objects.filter(types=constants.NEWS_TYPE_NEW,
                               is_valid=True)
    paginator = Paginator(news, page_size)
    page_data = paginator.page(page)
    return render(request, template_name, {
        'page_data': page_data

    })


def news_detail(request, pk, template_name='news_info.html'):
    """新闻详情"""
    # get_object_or_404找不到就返回404
    new_obj = get_object_or_404(News, pk=pk, is_valid=True)
    # 每查看一次，浏览次数+1，F在数据库层面进行修改
    new_obj.view_count = F('view_count') + 1
    new_obj.save()
    # 重新从数据库取数据
    new_obj.refresh_from_db()
    return render(request, template_name, {
        'new_obj': new_obj
    })


def verify_code(request):
    """验证码的显示"""
    # 得到这个验证码，不像别的视图函数一样，可以返回一个html页面，要想把验证码可以显示在前台
    # 页面，就用img标签显示（因为验证码是一个图片），用img的url属性
    # 验证码生成的时候存在session中，用户访问地址就能看到验证码
    client = VerifyCode(request)
    return client.gen_code()




