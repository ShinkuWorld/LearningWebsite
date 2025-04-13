# Generated by Django 5.1.7 on 2025-04-13 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0007_alter_course_chapter_chapter"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chapter",
            name="course",
        ),
        migrations.RemoveField(
            model_name="course",
            name="chapter",
        ),
        migrations.AddField(
            model_name="chapter",
            name="description",
            field=models.TextField(blank=True, verbose_name="章节描述"),
        ),
        migrations.AddField(
            model_name="course",
            name="chapters",
            field=models.ManyToManyField(
                related_name="courses", to="courses.chapter", verbose_name="课程章节"
            ),
        ),
    ]
