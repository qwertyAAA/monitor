"""
Django settings for monitor project.

Generated by 'django-admin startproject' using Django 1.11.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ud%@&3#9@zntn7^mfv!%1!w&bowh+i5q0pel6vteya_cr2rf^7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mail',
    'organization',
    'xadmin.apps.XadminConfig',
    'user_management.apps.UserManagementConfig',
    'permission',
    'menu_management',
    'SpiderDB',
    'fulltext_search',
    'report',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middlewares.xadminMiddleware.CheckXadminPermission',
    'permission.service.rbac.ValidPermission',
    'middlewares.all_requests.PushRequests',
]

ROOT_URLCONF = 'monitor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'middlewares.all_requests.get_online_requests_count',
                'middlewares.all_requests.base',
            ],
        },
    },
]

WSGI_APPLICATION = 'monitor.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库的类型
        'HOST': '10.25.116.62',  # 数据库的地址
        # 'HOST': 'localhost',  # 数据库的地址
        'PORT': 3306,
        'NAME': 'monitor',
        'USER': 'root',
        'PASSWORD': '123456',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',  # 数据库的类型
#         # 'HOST': '10.25.116.62',  # 数据库的地址
#         'HOST': 'localhost',  # 数据库的地址
#         'PORT': 3306,
#         'NAME': 'monitor',
#         'USER': 'root',
#         'PASSWORD': '123456',
#     }
# }

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

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# 缓存数据库配置，LOCATION这一项需要更改
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://10.25.116.62:6379/0",
        # "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Session 的引擎：db+缓存
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

STATIC_URL = '/static/'
# media配置，用户上传的文件都默认存放到当前文件夹下
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'media'),
]

# 配置邮箱发邮件的相关功能
"""
不可删除
"""
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# smtp服务的邮箱服务器
EMAIL_HOST = 'smtp.163.com'
# smtp服务固定的端口是25
EMAIL_PORT = 25
# 发送邮件的邮箱
EMAIL_HOST_USER = '18388627773@163.com'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = '163mail'
# 收件人看到的发件人 <此处要和发送邮件的邮箱相同>
EMAIL_FROM = '18388627773@163.com'
