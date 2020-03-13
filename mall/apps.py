from django.apps import AppConfig


class MallConfig(AppConfig):
    name = 'mall'
    # 在admin后台中显示模块的名字为商品模块
    verbose_name = '商品模块'
