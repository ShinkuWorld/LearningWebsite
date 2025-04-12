from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'chapters', views.ChapterViewSet, basename='chapter')

urlpatterns = [
    # 课程管理
    path('', views.CourseListCreateView.as_view(), name='course_list_create'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('<int:pk>/enroll/', views.CourseEnrollView.as_view(), name='course_enroll'),
    
    # 课程资源
    path('<int:course_pk>/resources/', views.CourseResourceListCreateView.as_view(), name='course_resource_list_create'),
    path('<int:course_pk>/resources/<int:pk>/', views.CourseResourceDetailView.as_view(), name='course_resource_detail'),
    
    # 作业管理
    path('<int:course_pk>/assignments/', views.AssignmentListCreateView.as_view(), name='assignment_list_create'),
    path('<int:course_pk>/assignments/<int:pk>/', views.AssignmentDetailView.as_view(), name='assignment_detail'),
    path('<int:course_pk>/assignments/<int:assignment_pk>/submit/', views.AssignmentSubmitView.as_view(), name='assignment_submit'),
    path('<int:course_pk>/assignments/<int:assignment_pk>/submissions/', views.AssignmentSubmissionListView.as_view(), name='submission_list'),
] + router.urls