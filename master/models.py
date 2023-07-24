from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator 
# Create your models here.
LVL = (
    ('Simple', 'Simple'),
    ('Medium', 'Medium'),
    ('Difficult', 'Difficult'),
)


class Course(models.Model):
    course_name = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course_name
    
class Subject(models.Model):
    course_name=models.ForeignKey(Course,on_delete=models.CASCADE)
    semesters = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(8)])
    subject_name = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject_name

class Question(models.Model):
    subjects = models.ForeignKey(Subject, on_delete=models.CASCADE)
    questions = models.TextField(max_length=2000)
    difficulty = models.CharField(choices=LVL, max_length=10)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.questions


class CustomerDetails(models.Model):
    basic_data = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=10,validators=[RegexValidator(r'^\d{10}$')])
    address = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    place = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now=True)

class QuestionPaper(models.Model):
    college=models.ForeignKey(User,on_delete=models.CASCADE)
    subjects = models.ForeignKey(Subject, on_delete=models.CASCADE)
    qstn=models.FileField(upload_to='media/quest/')
    created = models.DateTimeField(auto_now=True)

class FeedbackModel(models.Model):
    Name = models.CharField(max_length=50)
    Email = models.EmailField()
    Subject = models.CharField(max_length=100)
    Message = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Name