"""
关于Shinku项目的设置

"""
from pathlib import Path


# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 用于加密和验证的密钥
SECRET_KEY = "vpem6t1hvry7#+&g=pvs04lvbfvt6q-b$23-uvb=8cw*c7&l8h"

# DEBUG模式
DEBUG = True

# 允许访问Django应用的主机
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

# 应用程序定义
INSTALLED_APPS = [
    # 默认应用程序
    # 管理界面
    "django.contrib.admin",
    # 用户认证系统
    "django.contrib.auth",
    # 允许应用程序与Django的内容类型框架进行交互
    "django.contrib.contenttypes",
    # 会话管理系统
    "django.contrib.sessions",
    # 消息框架
    "django.contrib.messages",
    # 静态文件管理
    "django.contrib.staticfiles",

    # 自定义应用程序
    

    # 第三方应用程序
    # 用于解决跨域请求问题
    "corsheaders",
]

# 中间件设置
MIDDLEWARE = [
    # 跨域请求中间件
    "corsheaders.middleware.CorsMiddleware",
    # 防点击劫持中间件
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 安全中间件
    "django.middleware.security.SecurityMiddleware",
    # 会话中间件
    "django.contrib.sessions.middleware.SessionMiddleware",
    # 通用中间件
    "django.middleware.common.CommonMiddleware",
    # CSRF中间件
    "django.middleware.csrf.CsrfViewMiddleware",
    # 用户认证中间件
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # 消息中间件
    "django.contrib.messages.middleware.MessageMiddleware",
]

# 根URL配置
ROOT_URLCONF = "MainBackend.urls"

# 模板设置
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI应用程序
WSGI_APPLICATION = "Shinku.wsgi.application"

# 数据库配置
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",    
        "NAME": 'main', 
        "HOST": '127.0.0.1', 
        "PORT": 3306, 
        "USER": 'shinku',  
        "PASSWORD": 'shinku0721', 
    }
}

# 密码验证器
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# 国际化和时区设置
# 语言
LANGUAGE_CODE = "zh-hans"
# 时区
TIME_ZONE = "Asia/Shanghai"
# 国际化支持
USE_I18N = True
# 时区支持
USE_TZ = True

# 默认主键字段类型
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS 跨域配置
# CORS允许的头部
CORS_ALLOW_HEADERS = [
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
]
# CORS允许的 HTTP 方法
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
]
# CORS允许的源，用于跨域
CORS_ALLOWED_ORIGINS = [
    "localhost",
    "127.0.0.1",
]
# CORS是否运行携带cookies
CORS_ALLOW_CREDENTIALS = True 

# 存储目录设置


# 会话设置
# 使用数据库存储会话数据
SESSION_ENGINE = 'django.contrib.sessions.backends.db' 
# 会话Cookie的SameSite属性设置
SESSION_COOKIE_SAMESITE = 'None'
# 会话Cookie是否仅通过HTTPS传输
SESSION_COOKIE_SECURE = 'True'
# 会话过期时间为1小时
SESSION_COOKIE_AGE = 3600

# CSRF设置
# CSRF Cookie的域名设置
CSRF_COOKIE_DOMAIN = None 
# CSRF Cookie的路径设置 
CSRF_COOKIE_PATH = '/'
# CSRF Cookie是否仅通过HTTPS传输
CSRF_COOKIE_SECURE = True 
# CSRF Cookie是否仅通过HTTP访问
CSRF_COOKIE_HTTPONLY = False
# CSRF Cookie的SameSite属性设置
CSRF_COOKIE_SAMESITE = 'None'  
# CSRF Cookie的名称
CSRF_COOKIE_NAME = 'csrftoken'
# CSRF令牌在HTTP头中的名称
CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'
# 信任的源列表
CSRF_TRUSTED_ORIGINS = [
    'localhost',
    '127.0.0.1',
]

