# Generated by Django 5.1.7 on 2025-04-12 15:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0004_course_chapter"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="teacher",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"user_type": "teacher"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="teaching_courses",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
