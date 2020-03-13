"""
更新订单状态
订单超过半个小时不支付，取消订单，释放库存
"""
from django.core.management.base import BaseCommand


# 类名只能起这个，不能写别的
class Command(BaseCommand):
    help = """
        更新订单状态
        回收订单
    """
    # 使用help  python manage.py update --help
    # 本来就有的runserver python manage.py runserver --help
    # python manage.py help update（update命令的帮助）

    def add_arguments(self, parser):
        """
        添加命令的参数
        文档：
        https://docs.python.org/3/library/argparse.html
        1.回收所有超时未支付的订单
        python manage.py update --all
        2.指定回收某一个订单
        python manager.py update --one 20001
        :param parser:
        :return:
        """
        # 参数
        parser.add_argument(
            '--all',
            # 是store时python manage.py update --all后面要有参数
            # 是store_true时python manage.py update --all后面不用跟参数
            action='store',
            dest='all',
            default=False,
            help='回收所有超时未支付的订单'
        )

        parser.add_argument(
            '--one',
            action='store',
            dest='one',
            default=False,
            help='指定回收某一个订单'
        )

    # 这里面是处理逻辑
    def handle(self, *args, **options):
        if options['all']:
            # 打印信息
            self.stdout.write('开始回收订单')
            # 逻辑处理（在这个地方实现如何回收）
            # 处理逻辑比较复杂，先简单实现
            self.stdout.write('----------')
            self.stdout.write('处理完成')
        elif options['one']:
            self.stdout.write('开始回收订单{}'.format(options['one']))
        else:
            # 错误的信息
            self.stderr.write('指令异常')
