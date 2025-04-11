"""
项目URL配置

"""

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # 默认的Django后台管理页面
    path("admin/", admin.site.urls),
]
