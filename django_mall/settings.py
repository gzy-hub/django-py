"""
Django settings for django_mall project.

Generated by 'django-admin startproject' using Django 1.11.20.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 下载xadmin源码安装
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p@-_4ng&fm8hpfn#(lqe&cdmeau_+425dc@&$yw!vra%1jdplr'

# SECURITY WARNING: don't run with debug turned on in production!
# 生产模式False，调试模式True
# 发送邮件通知报错时，要为生产模式
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',  # django中的用户机制
    'django.contrib.contenttypes',  # 复合类型会用到
    'django.contrib.sessions',
    'django.contrib.messages',  # 给用户提示的消息，如果你删除商品，给你一个信息告诉你删除成功
    'django.contrib.staticfiles',
    # 富文本编辑器
    'ckeditor',
    'ckeditor_uploader',
    # django xadmin后台管理
    'xadmin',
    'crispy_forms',
    'reversion',
    'mall.apps.MallConfig',  # 商品模块
    'accounts.apps.AccountsConfig',  # 用户账户模块
    'system.apps.SystemConfig',  # 系统模块
    'mine.apps.MineConfig',  # 个人模块
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 在utils下的middleware有这么一个中间件，限制IP
    # 'utils.middleware.ip_middleware',
    # 'utils.middleware.MallAuthMiddleware',

]

ROOT_URLCONF = 'django_mall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            # 上下文
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 把constants文件中的常量配置到system下context_processors文件中，可以直接在
                # 前台页面中直接使用constants中的东西
                'system.context_processors.const',
                'mine.context_processors.shop_cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_mall.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_mall',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
# 修改admin后台管理的语言
# LANGUAGE_CODE = 'en-us'  # 英语
# 中文
LANGUAGE_CODE = 'zh-hans'

# TIME_ZONE = 'UTC'  # 时区
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# 新建完项目本来就有STATIC_URL
STATIC_URL = '/static/'
# 要想能访问static目录下的文件，需要进行下面的配置
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
# 自己上传的图片
MEDIA_ROOT = os.path.join(BASE_DIR, 'medias')
MEDIA_URL = '/medias/'
# 使用自定义的用户模型
AUTH_USER_MODEL = 'accounts.User'
# 退出用户登录去访问，用户地址列表等网址，会报错，需要配置这个属性，跳转到登录
# 表示用户在没有登录时访问添加了@login_required视图的网址时跳转到的页面
LOGIN_URL = '/accounts/user/login/'

# 富文本文件上传
CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'uploads')
# 设置异步请求的csrf
CSRF_USE_SESSIONS = False


# 邮件发送配置
EMAIL_HOST = 'smtp.qq.com'   # 发送邮件的服务器
EMAIL_HOST_USER = '1332088651@qq.com'
EMAIL_HOST_PASSWORD = 'xbtszpvwubbubaea'  # 授权码

# 如果页面报错，需要发邮件通知
SERVER_EMAIL = '1332088651@qq.com'   # 用哪个邮箱来发送
# 通知到谁
ADMINS = [('admin', '1332088651@qq.com')]  # 配置管理员，可以加多个，里面是一个元组

# 日志的配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # 日志的格式
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    # handlers决定了怎么处理日志
    'handlers': {
        # 写了一个handlers，命名为log_file
        'log_file': {
            # 级别
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            # 记录日志的地址
            'filename': os.path.join(BASE_DIR, 'log/debug.log'),
        },
        # 自定义一个只记录首页的
        'log_index_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': os.path.join(BASE_DIR, 'log/index.log'),
        },
        # 在控制台打印出来
        'console': {
            'level': 'DEBUG',
            # 'filters': ['require_debug_true'],   # 需要debug=True
            'class': 'logging.StreamHandler',
            # 'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            # 'filters': ['special']
        }
    },
    'loggers': {
        # django提供的内置的logger名字
        'django.db.backends': {
            'handlers': ['log_file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'index': {
            'handlers': ['log_index_file', 'console'],
            'level': 'DEBUG',
        }
    },
}