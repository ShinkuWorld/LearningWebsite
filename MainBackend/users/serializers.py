from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    user_type = serializers.CharField(required=True, error_messages={'required': '请选择用户类型'})
    email = serializers.EmailField(required=True, error_messages={'required': '请输入邮箱'})

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'user_type', 'phone', 'student_id', 'teacher_id']

    def validate_user_type(self, value):
        if value == 'admin':
            raise serializers.ValidationError("不允许注册管理员账号")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get('username', ''),
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type'],
            phone=validated_data.get('phone', ''),
            student_id=validated_data.get('student_id', ''),
            teacher_id=validated_data.get('teacher_id', '')
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type', 'phone', 'student_id', 'teacher_id']
        read_only_fields = ['id', 'username', 'user_type']