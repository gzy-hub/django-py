
"""
生成验证码：
1.准备素材
字体（ttf)，文字内容，颜色，干扰线
2.画验证码
pip install Pillow   random
创建图片
记录文字内容， django session【指的是服务器，python代码】
session原理：登录之后，浏览器给你一个字符串，放在浏览器的cookie【指的是浏览器】中，下次
请求就带上，就知道是你了，服务器上把字符串对应的信息（如姓名等）存在session中
（1）第一次请求， cookie + session对应关系生成
（2）第二次请求，携带了cookie，找到对应的session【提交表单】
     请求带上验证码参数与session中的验证码进行比较
3、io文件流（用户访问某一个url地址，然后把图片写到那个里面去，访问地址就可以看到图片）
BytesIO
"""
import os
import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse

from django_mall import settings


class VerifyCode(object):
    """验证码类"""
    # dj_request指的是请求对象（需要用到session）
    def __init__(self, dj_request):
        self.dj_request = dj_request
        # 验证码长度
        self.code_len = 4
        # 验证码图片尺寸
        self.img_width = 100
        self.img_height = 30

        # django中的session的名称
        self.session_key = 'verify_code'

    def gen_code(self):
        """生成验证码"""
        # 1、使用随机数生成验证码字符
        code = self._get_vcode()
        # 2、把验证码存在session中，dj_request有一个session对象，可以把session理解为一个字典
        # 给指定一个名字，把code存到里面
        self.dj_request.session[self.session_key] = code
        # 3、准备随机元素（背景颜色、验证码文字的颜色、干扰线）
        font_color = ['black', 'darkblue', 'darkred', 'brown', 'green', 'darkmagenta', 'cyan', 'darkcyan']
        # RGB随机背景色
        bg_color = (random.randrange(230, 255), random.randrange(230, 255), random.randrange(230, 255))
        # 字体路径
        font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'timesbi.ttf')

        # 创建图片，'RGB'模型，宽度和高度，背景颜色
        im = Image.new('RGB', (self.img_width, self.img_height), bg_color)
        # 画笔
        draw = ImageDraw.Draw(im)

        # 画干扰线
        # 线是两个点之间（0,0）（self.img_width, self.img_height）,fill指的是颜色，width宽度
        # draw.line((0, 0, self.img_width, self.img_height), fill=line_color, width=5)
        # 随机条数，到底画几条
        for i in range(random.randrange(1, int(self.code_len / 2) + 1)):
            # 线条的颜色
            line_color = random.choice(font_color)
            # 线条的位置
            point = (
                random.randrange(0, self.img_width * 0.2),
                random.randrange(0, self.img_height),
                random.randrange(self.img_width - self.img_width * 0.2, self.img_width),
                random.randrange(0, self.img_height))
            # 线条的宽度
            width = random.randrange(1, 4)
            draw.line(point, fill=line_color, width=width)

        # 画验证码
        # 进行循环操作，对验证码每个值进行编写，enumerate枚举函数，index表示第几个验证码
        for index, char in enumerate(code):
            code_color = random.choice(font_color)
            # 指定字体
            font_size = random.randrange(15, 25)
            # 参数为字体的位置和字体大小
            font = ImageFont.truetype(font_path, font_size)
            # index * self.img_width / self.code_len宽度偏移，
            # random.randrange(0, self.img_height / 3)高度随机
            point = (index * self.img_width / self.code_len,
                     random.randrange(0, self.img_height / 3))
            # point位置，font字体，fill颜色，char为内容，就是code
            draw.text(point, char, font=font, fill=code_color)

        # 写到文件流中去
        buf = BytesIO()
        im.save(buf, 'gif')
        # 返回到页面去，是image/gif的类型
        return HttpResponse(buf.getvalue(), 'image/gif')

    # 生成验证码的4个字
    def _get_vcode(self):
        random_str = 'ABCDEFGHIJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789'
        # 这是一个列表
        code_lsit = random.sample(list(random_str), self.code_len)
        code = ''.join(code_lsit)
        return code

    def validate_code(self, code):
        """验证验证码是否正确"""
        # 1、转变大小写
        code = str(code).lower()
        vcode = self.dj_request.session.get(self.session_key, '')
        # if vcode.lower == code:
        #     return True
        # return False
        # 可直接用下面的写法
        return vcode.lower() == code


if __name__ == '__main__':
    client = VerifyCode(None)
    client.gen_code()