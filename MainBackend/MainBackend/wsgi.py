"""
项目的WSGI配置。

将WSGI可调用对象作为名为'application'的模块级变量公开。
"""

import os

from django.core.wsgi import get_wsgi_application

# 设置默认的Django设置模块
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Shinku.settings")

# 获取Django应用的WSGI应用实例
application = get_wsgi_application()
