from rest_framework import serializers
from django.utils import timezone
from .models import Course, CourseResource, Assignment, AssignmentSubmission, CourseContent, Chapter
from users.models import User

class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'user_type']

class CourseSerializer(serializers.ModelSerializer):
    teacher = UserBriefSerializer(read_only=True)
    students = UserBriefSerializer(many=True, read_only=True)
    student_count = serializers.SerializerMethodField()
    chapter_display = serializers.SerializerMethodField()
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(user_type='teacher'),
        source='teacher',
        write_only=True,
        required=True
    )

    class Meta:
        model = Course
        fields = ['id', 'name', 'teacher', 'description', 'created_at', 'students', 'student_count', 'chapters', 'teacher_id']
        extra_kwargs = {
            'name': {'required': True},
            'students': {'required': False},
            'chapters': {'required': False}
        }

    def get_chapter_display(self, obj):
        return obj.get_chapter_display()

    def get_student_count(self, obj):
        return obj.students.count()

class CourseResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseResource
        fields = ['id', 'course', 'title', 'file', 'resource_type', 'upload_time']
        extra_kwargs = {
            'course': {'read_only': True},
            'file': {'required': False},
            'upload_time': {'read_only': True},
            'title': {'required': False},
            'resource_type': {'required': False}
        }

class ChapterChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'name', 'description', 'order', 'created_at']
        read_only_fields = ['created_at']
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': False},
            'order': {'required': False}
        }

class AssignmentSerializer(serializers.ModelSerializer):
    submission_count = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = ['id', 'course', 'title', 'description', 'deadline', 'created_at', 'submission_count']

    def get_submission_count(self, obj):
        return obj.submissions.count()

class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student = UserBriefSerializer(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = ['id', 'assignment', 'student', 'file', 'submit_time', 'score', 'comment', 'status']
        read_only_fields = ['score', 'comment']

    def validate(self, data):
        if self.instance and self.instance.status == 'graded':
            raise serializers.ValidationError('已批改的作业不能修改')
        return data

    def create(self, validated_data):
        assignment = validated_data['assignment']
        if assignment.deadline < timezone.now():
            validated_data['status'] = 'late'
        else:
            validated_data['status'] = 'pending'
        return super().create(validated_data)

class CourseContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseContent
        fields = ['id', 'course', 'title', 'content', 'order', 'created_at']
        read_only_fields = ['course', 'created_at']