from rest_framework import viewsets, status, generics, pagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from .models import Course, CourseContent, Chapter
from .serializers import ChapterChoiceSerializer, CourseSerializer, CourseContentSerializer

class CourseListCreateView(generics.ListCreateAPIView):
    """
    课程列表和创建API
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    课程详情、更新和删除API
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class ChapterViewSet(viewsets.ModelViewSet):
    """
    课程章节管理API，仅管理员可访问
    """
    queryset = Chapter.objects.all()
    serializer_class = ChapterChoiceSerializer
    permission_classes = [IsAdminUser]
    pagination_class = pagination.PageNumberPagination
    
    def list(self, request):
        """获取所有课程章节"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """创建新的课程章节"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """删除课程章节"""
        chapter = self.get_object()
        chapter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CourseEnrollView(generics.CreateAPIView):
    """
    课程注册API
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    def create(self, request, *args, **kwargs):
        course = self.get_object()
        user = request.user
        if course.students.filter(id=user.id).exists():
            return Response({'error': '您已经注册过该课程'}, status=status.HTTP_400_BAD_REQUEST)
        
        course.students.add(user)
        return Response({'message': '注册成功'}, status=status.HTTP_201_CREATED)

class CourseResourceListCreateView(generics.ListCreateAPIView):
    """
    课程资源列表和创建API
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    def get_queryset(self):
        course_pk = self.kwargs.get('course_pk')
        return super().get_queryset().filter(pk=course_pk)

class CourseResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    课程资源详情、更新和删除API
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    def get_object(self):
        course_pk = self.kwargs.get('course_pk')
        resource_pk = self.kwargs.get('pk')
        return super().get_queryset().filter(pk=course_pk).first()

class AssignmentListCreateView(generics.ListCreateAPIView):
    """
    课程作业列表和创建API
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    def get_queryset(self):
        course_pk = self.kwargs.get('course_pk')
        return super().get_queryset().filter(pk=course_pk)

class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    课程作业详情、更新和删除API
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    def get_object(self):
        course_pk = self.kwargs.get('course_pk')
        assignment_pk = self.kwargs.get('pk')
        return super().get_queryset().filter(pk=course_pk).first()

class AssignmentSubmissionListView(generics.ListAPIView):
    """
    作业提交列表API
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    def get_queryset(self):
        course_pk = self.kwargs.get('course_pk')
        assignment_pk = self.kwargs.get('assignment_pk')
        return super().get_queryset().filter(pk=course_pk)

class AssignmentSubmitView(generics.CreateAPIView):
    """
    作业提交API
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    def create(self, request, *args, **kwargs):
        course_pk = self.kwargs.get('course_pk')
        assignment_pk = self.kwargs.get('assignment_pk')
        course = super().get_queryset().filter(pk=course_pk).first()
        
        # 这里可以添加作业提交逻辑
        return Response({'message': '作业提交成功'}, status=status.HTTP_201_CREATED)

class CourseContentListCreateView(generics.ListCreateAPIView):
    """
    课程内容列表和创建API
    """
    queryset = CourseContent.objects.all()
    serializer_class = CourseContentSerializer
    
    def get_queryset(self):
        course_pk = self.kwargs.get('course_pk')
        return super().get_queryset().filter(course_id=course_pk)

class CourseContentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    课程内容详情、更新和删除API
    """
    queryset = CourseContent.objects.all()
    serializer_class = CourseContentSerializer
    
    def get_object(self):
        course_pk = self.kwargs.get('course_pk')
        content_pk = self.kwargs.get('pk')
        return super().get_queryset().filter(course_id=course_pk, pk=content_pk).first()
