# Generated by Django 4.2 on 2023-05-15 20:46

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=60)),
                ('created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeedbackModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Email', models.EmailField(max_length=254)),
                ('Subject', models.CharField(max_length=100)),
                ('Message', models.TextField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semesters', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('subject_name', models.CharField(max_length=60)),
                ('created', models.DateTimeField(auto_now=True)),
                ('course_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.course')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionPaper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qstn', models.FileField(upload_to='media/quest/')),
                ('created', models.DateTimeField(auto_now=True)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subjects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questions', models.TextField(max_length=500)),
                ('difficulty', models.CharField(choices=[('Simple', 'Simple'), ('Medium', 'Medium'), ('Difficult', 'Difficult')], max_length=10)),
                ('created', models.DateTimeField(auto_now=True)),
                ('subjects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.subject')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$')])),
                ('address', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=6)),
                ('place', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now=True)),
                ('basic_data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
