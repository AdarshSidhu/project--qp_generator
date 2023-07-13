from django.contrib import admin
from .models import Question,Subject,CustomerDetails,QuestionPaper,Course
# Register your models here.
admin.site.register(Question)
admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(CustomerDetails)
admin.site.register(QuestionPaper)