from django.contrib import admin
from .models import Course, CourseResource, Assignment, AssignmentSubmission, GradeHistory, CourseContent, Chapter


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'teacher__username')
    raw_id_fields = ('teacher', 'students')


@admin.register(CourseResource)
class CourseResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'resource_type', 'upload_time')
    list_filter = ('resource_type', 'upload_time')
    search_fields = ('title', 'course__name')
    raw_id_fields = ('course',)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'deadline', 'created_at')
    list_filter = ('deadline', 'created_at')
    search_fields = ('title', 'course__name')
    raw_id_fields = ('course',)


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'status', 'score', 'submit_time')
    list_filter = ('status', 'submit_time')
    search_fields = ('assignment__title', 'student__username')
    raw_id_fields = ('assignment', 'student', 'last_graded_by')


@admin.register(GradeHistory)
class GradeHistoryAdmin(admin.ModelAdmin):
    list_display = ('submission', 'score', 'graded_by', 'graded_at')
    list_filter = ('graded_at',)
    search_fields = ('submission__assignment__title', 'graded_by__username')
    raw_id_fields = ('submission', 'graded_by')


@admin.register(CourseContent)
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'course__name')
    raw_id_fields = ('course',)


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
