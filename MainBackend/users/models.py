from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('teacher', '教师'),
        ('student', '学生'),
    )
    
    username = models.CharField('用户名', max_length=150)
    email = models.EmailField('邮箱', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    user_type = models.CharField('用户类型', max_length=10, choices=USER_TYPE_CHOICES)
    phone = models.CharField('手机号', max_length=11, blank=True)
    student_id = models.CharField('学号', max_length=20, blank=True)
    teacher_id = models.CharField('教师工号', max_length=20, blank=True)
    is_logged_in = models.BooleanField('登录状态', default=False)
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.email
