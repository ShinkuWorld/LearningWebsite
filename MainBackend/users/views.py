from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserRegisterSerializer, UserProfileSerializer

def api_response(code=200, message="success", data=None):
    return Response({
        "code": code,
        "message": message,
        "data": data
    })

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data.get('email')
        if User.objects.filter(email=email).exists():
            return api_response(
                code=status.HTTP_400_BAD_REQUEST,
                message="该邮箱已被注册",
                data=None
            )
            
        user = serializer.save()
        return api_response(
            message="注册成功",
            data=UserProfileSerializer(user).data
        )

class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = request.user
        user.is_logged_in = False
        user.save()
        return api_response(message="注销成功")

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(data=serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return api_response(
            message="更新成功",
            data=serializer.data
        )

class StudentListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(user_type='student')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return api_response(data=serializer.data)

class TeacherListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(user_type='teacher')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return api_response(data=serializer.data)
