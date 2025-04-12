from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Course
from .serializers import ChapterChoiceSerializer, CourseSerializer

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

class ChapterViewSet(viewsets.ViewSet):
    """
    课程分类管理API
    """
    
    def list(self, request):
        """获取所有课程分类选项"""
        choices = [{'value': value, 'display': display} for value, display in Course.CHAPTER_CHOICES]
        serializer = ChapterChoiceSerializer(choices, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """添加新的课程分类选项"""
        serializer = ChapterChoiceSerializer(data=request.data)
        if serializer.is_valid():
            value = serializer.validated_data['value']
            display = serializer.validated_data['display']
            Course.add_chapter_choice(value, display)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """删除课程分类选项"""
        value = request.data.get('value')
        if not value:
            return Response({'error': 'value参数是必须的'}, status=status.HTTP_400_BAD_REQUEST)
        
        Course.remove_chapter_choice(value)
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
