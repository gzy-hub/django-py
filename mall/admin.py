from django.contrib import admin

# Register your models here.
from mall.forms import ProductAdminForm
from mall.models import Product, Classify, Tag

from utils.admin_actions import set_invalid, set_valid


# 方式1：注册到后台管理
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """商品信息管理"""
    # 要在前台页面显示的商品的字段
    list_display = ['name', 'types', 'price', 'status', 'is_valid']
    # 修改分页数据的大小，每页显示多少条
    list_per_page = 5
    # 在原来商品列表的右边出现一个筛选的，快捷搜索字段
    list_filter = ('status',)
    # 排除掉某些字段，使之不能编辑，在编辑界面也不可见
    # exclude = ['ramain_count']
    # 不可编辑，但是在界面上是可见的，只读
    readonly_fields = ['ramain_count']
    # 配置到商品上
    # 这是隐式传递的，因为actions是定义在ProductAdmin中，
    # 而这个ProductAdmin正是继承自admin.ModelAdmin，且通过register( )的方式
    # 进行Product的管理，所以actions中方法名称会根据所在类识别出modeladmin的所属，
    # 进而关联到所管理的Product类，但是这条传递线路是被django封装好的，
    # 我们无法显式的看到。
    actions = [set_invalid, set_valid]
    # 在form表单中自己定义的表单，自定义的表单
    form = ProductAdminForm


# 方式2：注册到后台管理
# admin.site.register(Product, ProductAdmin)


@admin.register(Classify)
class ClassifyAdmin(admin.ModelAdmin):
    """商品分类管理"""
    list_display = ('parent', 'name', 'code', 'is_valid')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """商品标签管理"""
    list_display = ('name', 'code', 'is_valid')