from django.db import models
from django.utils import timezone
from users.models import User

class Course(models.Model):
    STATUS_CHOICES = (
        ('active', '进行中'),
        ('archived', '已结束')
    )
    CHAPTER_CHOICES = (
        ('basic', '基础知识'),
        ('data_structure', '数据结构'),
        ('algorithm', '算法'),
        ('advanced', '高级主题'),
    )
    
    @classmethod
    def add_chapter_choice(cls, value, display):
        """添加新的章节分类选项"""
        if not hasattr(cls, '_chapter_choices_cache'):
            cls._chapter_choices_cache = dict(cls.CHAPTER_CHOICES)
        cls._chapter_choices_cache[value] = display
        cls.CHAPTER_CHOICES = tuple(cls._chapter_choices_cache.items())
    
    @classmethod
    def remove_chapter_choice(cls, value):
        """删除章节分类选项"""
        if not hasattr(cls, '_chapter_choices_cache'):
            cls._chapter_choices_cache = dict(cls.CHAPTER_CHOICES)
        if value in cls._chapter_choices_cache:
            del cls._chapter_choices_cache[value]
            cls.CHAPTER_CHOICES = tuple(cls._chapter_choices_cache.items())

    name = models.CharField('课程名称', max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='teaching_courses', limit_choices_to={'user_type': 'teacher'})
    description = models.TextField('课程描述', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    students = models.ManyToManyField(User, related_name='enrolled_courses', limit_choices_to={'user_type': 'student'})
    status = models.CharField('课程状态', max_length=10, choices=STATUS_CHOICES, default='active')
    chapter = models.CharField('章节分类', max_length=20, choices=CHAPTER_CHOICES, default='basic')

    def archive_course(self):
        """归档课程及其相关作业"""
        self.status = 'archived'
        self.save()
        # 更新所有未提交的作业状态为已结束
        for assignment in self.assignments.all():
            for submission in assignment.submissions.filter(status='not_submitted'):
                submission.status = 'archived'
                submission.save()

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class CourseResource(models.Model):
    RESOURCE_TYPE_CHOICES = (
        ('ppt', 'PPT'),
        ('document', '文档'),
        ('video', '视频'),
        ('other', '其他'),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField('资源标题', max_length=100)
    file = models.FileField('资源文件', upload_to='course_resources/')
    resource_type = models.CharField('资源类型', max_length=10, choices=RESOURCE_TYPE_CHOICES)
    upload_time = models.DateTimeField('上传时间', auto_now_add=True)

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField('作业标题', max_length=100)
    description = models.TextField('作业描述')
    deadline = models.DateTimeField('截止时间')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '作业'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class GradeHistory(models.Model):
    """作业评分历史记录"""
    submission = models.ForeignKey('AssignmentSubmission', on_delete=models.CASCADE, related_name='grade_histories')
    score = models.FloatField('得分')
    comment = models.TextField('评语', blank=True)
    graded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grading_histories')
    graded_at = models.DateTimeField('评分时间', auto_now_add=True)

    class Meta:
        verbose_name = '评分历史'
        verbose_name_plural = verbose_name
        ordering = ['-graded_at']

    def __str__(self):
        return f'{self.submission} - {self.score}分 - {self.graded_at}'

class AssignmentSubmission(models.Model):
    STATUS_CHOICES = (
        ('not_submitted', '未提交'),
        ('pending', '待批改'),
        ('graded', '已批改'),
        ('late', '逾期提交'),
        ('archived', '已归档')
    )

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignment_submissions', limit_choices_to={'user_type': 'student'})
    file = models.FileField('作业文件', upload_to='assignment_submissions/')
    submit_time = models.DateTimeField('提交时间', auto_now_add=True)
    score = models.FloatField('得分', null=True, blank=True)
    comment = models.TextField('评语', blank=True)
    status = models.CharField('状态', max_length=13, choices=[('submitted', '已提交'), ('graded', '已评分'), ('pending', '待处理')])
    last_graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_submissions')
    last_graded_at = models.DateTimeField('最后评分时间', null=True, blank=True)

    class Meta:
        verbose_name = '作业提交'
        verbose_name_plural = verbose_name
        unique_together = ['assignment', 'student']

    def __str__(self):
        return f'{self.student.username} - {self.assignment.title}'

    def save(self, *args, **kwargs):
        if not self.pk:  # 新创建的提交
            if self.assignment.deadline < timezone.now():
                self.status = 'late'
            else:
                self.status = 'pending'
        super().save(*args, **kwargs)

    def grade(self, score, comment, graded_by):
        if self.status not in ['pending', 'late']:
            raise ValueError('只能对待批改或逾期的作业进行评分')
        
        # 创建评分历史记录
        GradeHistory.objects.create(
            submission=self,
            score=score,
            comment=comment,
            graded_by=graded_by
        )

        # 更新作业提交状态
        self.score = score
        self.comment = comment
        self.status = 'graded'
        self.last_graded_by = graded_by
        self.last_graded_at = timezone.now()
        self.save()

        # TODO: 发送通知给学生（需要实现通知系统）
