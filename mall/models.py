import uuid

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor.fields import RichTextField
from django.db.models import F

from accounts.models import User
from system.models import ImageFile
from utils import constants


class Classify(models.Model):
    """商品分类"""
    uid = models.UUIDField('分类ID', default=uuid.uuid4, editable=True)
    # 一个分类下面可能有子类，子类下面还有子类，一对多的关系，如何实现，
    # 自己关联自己
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)
    img = models.ImageField('分类主图', upload_to='classify')
    # 给程序去使用
    code = models.CharField('编码', max_length=32, null=True, blank=True)
    name = models.CharField('名称', max_length=12)
    desc = models.CharField('描述', max_length=64, null=True, blank=True)
    reorder = models.SmallIntegerField('排序', default=0)
    is_valid = models.BooleanField('是否有效', default=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = 'mall_classify'
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'
        ordering = ['-reorder']

    def __str__(self):
        return '{}:{}'.format(self.code, self.name)


class Tag(models.Model):
    """商品的标签"""
    uid = models.UUIDField('标签ID', default=uuid.uuid4, editable=True)
    img = models.ImageField('主图', upload_to='tags', null=True, blank=True)
    code = models.CharField('编码', max_length=32, null=True, blank=True)
    name = models.CharField('名称', max_length=12)
    reorder = models.SmallIntegerField('排序', default=0)
    is_valid = models.BooleanField('是否有效', default=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = 'mall_tag'
        verbose_name = '商品标签'
        verbose_name_plural = '商品标签'
        ordering = ['-reorder']

    def __str__(self):
        return '{}:{}'.format(self.code, self.name)


class Product(models.Model):
    """商品"""
    # uuid生成随机的字符串，不会重复，editable不能在编辑，使之不能编辑，在admin编辑界面不可见
    uid = models.UUIDField('商品ID', default=uuid.uuid4, editable=False)
    name = models.CharField('商品名称', max_length=128)
    desc = models.CharField('简单描述', max_length=256, null=True, blank=True)
    # content = models.TextField('商品描述')
    # 富文本，让图片和文字都可以显示，安装了pip install django-ckeditor富文本
    content = RichTextField('商品描述')

    types = models.SmallIntegerField('商品类型',
                                     choices=constants.PRODUCT_TYPES_CHOICES,
                                     default=constants.PRODUCT_TYPE_ACTUAL)
    price = models.IntegerField('兑换价格（积分兑换）')
    origin_price = models.FloatField('原价')
    img = models.ImageField('主图', upload_to='%Y%m/product')
    buy_link = models.CharField('购买链接', max_length=256, null=True, blank=True)
    reorder = models.SmallIntegerField('排序', default=0)
    status = models.SmallIntegerField('商品状态', default=constants.PRODUCT_STATUS_LOST,
                                      choices=constants.PRODUCT_STATUS_CHOICES)

    sku_count = models.IntegerField('库存', default=0)
    ramain_count = models.IntegerField('剩余库存', default=0)
    view_count = models.IntegerField('浏览次数', default=0)
    score = models.FloatField('商品评分', default=10.0)

    is_valid = models.BooleanField('是否有效', default=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    tags = models.ManyToManyField(Tag, verbose_name='标签',
                                  related_name='tags',
                                  null=True,
                                  blank=True)
    classes = models.ManyToManyField(Classify, verbose_name='分类',
                                     related_name='classes',
                                     null=True,
                                     blank=True)
    # 反向关联到图片表，related_query_name可以直接拿到商品对象可以.banners，直接拿到Image里面的字段
    banners = GenericRelation(ImageFile, verbose_name='banner图',
                              related_query_name='banners')

    class Meta:
        db_table = 'mall_product'
        # 在admin后台中显示模型的名称为：商品信息，只加verbose_name会显示为商品信息s
        # 加上verbose_name_plural会显示为商品信息
        verbose_name = '商品信息'
        verbose_name_plural = '商品信息'
        ordering = ['-reorder']

    def update_store_count(self, count):
        """更改商品的库存信息"""
        # ramain_count剩余库存
        # 传入的count可能是负数，所以用abs求一下绝对值
        self.ramain_count = F('ramain_count') - abs(count)
        # 保存
        self.save()
        # 刷新数据库
        self.refresh_from_db()

    # 在admin中修改商品完成后，返回的信息返回商品的名字
    def __str__(self):
        return self.name














