from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # 用户认证
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    
    # 用户管理
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('teachers/', views.TeacherListView.as_view(), name='teacher_list'),
]