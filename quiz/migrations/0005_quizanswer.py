# Generated by Django 4.1.4 on 2023-01-21 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0004_quizchoice'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.ForeignKey(db_column='account_id', on_delete=django.db.models.deletion.CASCADE,
                                                 related_name='answer_account', to=settings.AUTH_USER_MODEL)),
                ('quiz_id', models.ForeignKey(db_column='quiz_id', on_delete=django.db.models.deletion.CASCADE,
                                              related_name='answer_quiz', to='quiz.quiz')),
                ('question', models.TextField()),
                ('is_correct', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'quiz_answers',
            },
        ),
    ]
