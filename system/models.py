from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

from utils import constants


class Slider(models.Model):
    """系统轮播图"""
    name = models.CharField('名称', max_length=32)
    desc = models.CharField('描述', max_length=100, null=True, blank=True)
    types = models.SmallIntegerField('展现位置',
                                    choices=constants.SLIDER_TYPE_CHOICES,
                                    default=constants.SLIDER_TYPE_INDEX)
    # 会自动创建文件夹
    img = models.ImageField('图片', upload_to='slider')
    # help_text文字提示
    reorder = models.SmallIntegerField('排序', default=0, help_text='数字越大，越靠前')
    start_time = models.DateTimeField('生效开始时间', null=True, blank=True)
    end_time = models.DateTimeField('生效结束时间', null=True, blank=True)

    target_url = models.CharField('跳转地址', max_length=255, null=True, blank=True)
    is_valid = models.BooleanField('是否删除', default=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最后修改时间', auto_now=True)

    class Meta:
        db_table = 'system_slider'
        verbose_name = '轮播图'
        verbose_name_plural = '轮播图'
        # 排序
        ordering = ['-reorder']


class News(models.Model):
    """新闻及通知"""
    types = models.SmallIntegerField('类型', choices=constants.NEWS_TYPE_CHOICES,
                                     default=constants.NEWS_TYPE_NEW)
    title = models.CharField('标题', max_length=255)
    content = models.TextField('内容')
    reorder = models.SmallIntegerField('排序', default=0, help_text='数字越大，越靠前')
    start_time = models.DateTimeField('生效开始时间', null=True, blank=True)
    end_time = models.DateTimeField('生效结束时间', null=True, blank=True)
    view_count = models.IntegerField('浏览次数', default=0)

    is_top = models.BooleanField('是否置顶', default=False)
    is_valid = models.BooleanField('是否删除', default=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最后修改时间', auto_now=True)

    class Meta:
        db_table = 'system_news'
        verbose_name = '新闻及通知'
        verbose_name_plural = '新闻及通知'
        ordering = ['-reorder']


class ImageFile(models.Model):
    """图片表"""
    # 上传图片，一个文件夹下图片数量是有限的，已月份为单位一个文件夹
    img = models.ImageField('图片', upload_to='%Y%m/images/')
    summary = models.CharField('图片名称', max_length=200)

    # 符合关联
    # 图片是和其他类型关联的
    content_type = models.ForeignKey(ContentType)
    # 关联到哪个商品
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    is_valid = models.BooleanField('是否有效', default=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = 'system_images'
        verbose_name = '图片表'
        verbose_name_plural = '图片表'
