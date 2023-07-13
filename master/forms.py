from  django import forms
from .models import Question, Subject, CustomerDetails, QuestionPaper, FeedbackModel,Course
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class DateInput(forms.DateInput):
    input_type = 'date'


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = CustomerDetails
        exclude = ('basic_data', 'created',)



class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        exclude = ('username', 'password')


class QForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ('created','subjects')

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('created',)


class SubForm(forms.ModelForm):
    class Meta:
        model = Subject
        exclude = ('created','course_name')

class QuestionSubForm(forms.ModelForm):
    class Meta:
        model = QuestionPaper
        exclude = ('created',)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedbackModel
        exclude = ('created_at',)
