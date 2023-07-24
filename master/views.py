import random
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.contrib.auth.models import User
from django.http import HttpResponse
from master.forms import QForm, SubForm, QuestionSubForm, CustomerForm, LoginForm, UserForm, FeedbackForm, CourseForm
from master.models import Question, Subject, CustomerDetails, QuestionPaper, FeedbackModel, Course
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import FormView, View, ListView, CreateView, TemplateView, UpdateView, DeleteView, DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from datetime import datetime


class QuestionC(CreateView):
    template_name = 'question.html'
    model = Question
    form_class = QForm
    success_url = '/addqn'
    success_message = ' Question created successfully'


class Coursecreation(CreateView):
    template_name = 'question.html'
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy('createcourse')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Course created successfully.')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Failed to create course. Please try again.')
        return response


class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, pk=self.kwargs.get('pk'))
        subjects = Subject.objects.filter(course_name=course)
        context['subjects'] = subjects
        return context


def create_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == 'POST':
        form = SubForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.course_name = course
            subject.save()
            messages.success(request, 'Subject created successfully.')
            return redirect('create-course', course_id=course_id)
        else:
            messages.error(request, 'Failed to create subject. Please check your input.')
    else:
        form = SubForm()

    return render(request, 'create_subject.html', {'form': form})


class Subjectview(ListView):
    template_name = 'sublist.html'
    model = Subject
    context_object_name = 'list'
    queryset = Subject.objects.all()


class SubjectDetailView(DetailView):
    model = Subject
    template_name = 'course_detail2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = get_object_or_404(Subject, pk=self.kwargs.get('pk'))
        newquestion = Question.objects.filter(subjects=subject)
        context['newquestion'] = newquestion
        return context


def create_question(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)

    if request.method == 'POST':
        form = QForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.subjects = subject
            question.save()
            messages.success(request, 'Question created successfully.')
            return redirect('create-question', subject_id=subject_id)
        else:
            messages.error(request, 'Failed to create subject. Please check your input.')
    else:
        form = QForm()

    return render(request, 'create_subject.html', {'form': form})


class About(TemplateView):
    template_name = 'about.html'


class Error(TemplateView):
    template_name = '404.html'


class Courcec(CreateView):
    template_name = 'question.html'
    model = Subject
    form_class = SubForm
    success_url = '/addcourse'


class Courseview(ListView):
    template_name = 'viewcourse.html'
    model = Course
    context_object_name = 'list'
    queryset = Course.objects.all()


def qlist(request):
    products = list(Subject.objects.all())

    return render(request, 'qlist.html', {'products': products})


class Home(TemplateView):
    template_name = 'index.html'


class Signup(FormView):
    template_name = 'signup.html'
    form_class = UserForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        user_form = self.get_form(form_class)
        cust_form = CustomerForm()
        return self.render_to_response(self.get_context_data(form1=user_form, form2=cust_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        user_form = self.get_form(form_class)
        cust_form = CustomerForm(self.request.POST)
        if (user_form.is_valid() and cust_form.is_valid()):
            return self.form_valid(user_form, cust_form)
        else:
            return self.form_invalid(user_form, cust_form)

    def form_valid(self, user_form, cust_form):
        self.object = user_form.save()  # User model save
        self.object.is_staff = False  # edit user object
        self.object.save()
        cust_obj = cust_form.save(commit=False)  # Customer Model save(contact,address,place)
        cust_obj.basic_data = self.object  # saving OneToOnefield ,edit cust_obj
        cust_obj.save()
        messages.success(self.request, 'College has been registered  successfully!')
        return super(Signup, self).form_valid(user_form)

    def form_invalid(self, user_form, cust_form):
        messages.error(self.request, 'Your form submission failed. Please check the error messages.')
        return self.render_to_response(self.get_context_data(form1=user_form, form2=cust_form))

    def get_success_url(self, **kwargs):
        return ('/signup')


class Login(View):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                user_obj = User.objects.get(username=request.user)
                cust = CustomerDetails.objects.get(basic_data=user_obj)
            except:
                user_obj = None
                cust = None
            if request.user.is_superuser:
                messages.success(request, 'Logged in successfully as a superuser.')
                return redirect('/home')
            elif cust:
                messages.success(request, 'Logged in successfully as a college admin.')
                return redirect('/profile/')
            else:
                messages.warning(request, 'Unable to log in. Please try again.')
                return redirect('/login/')
        else:
            messages.warning(request, 'Invalid username or password. Please try again.')
            return redirect('/login/')


class Profile(View):
    template_name = 'profile.html'

    def get(self, request):
        uname = request.user
        user_obj = User.objects.get(username=uname)
        cust_obj = CustomerDetails.objects.get(basic_data=user_obj)
        context = {'customer': cust_obj
                   # 'user': user_obj
                   }
        return render(request, self.template_name, context)


class ProfileUpdate(UpdateView):
    template_name = 'question.html'
    model = CustomerDetails
    fields = ['contact', 'address', 'pincode', 'place']
    success_url = '/profile/'


class NewFeedbackView(CreateView):
    template_name = 'contact.html'
    model = FeedbackModel
    form_class = FeedbackForm
    success_url = '/contact'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your form has been submitted successfully!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'There was an error submitting your form. Please try again.')
        return response


class Feedbacks(ListView):
    template_name = 'feedlist.html'
    model = FeedbackModel
    context_object_name = 'list'
    queryset = FeedbackModel.objects.order_by('-created_at')


class Colleges(ListView):
    model = User
    template_name = 'users.html'
    queryset = User.objects.filter(is_staff=False)
    context_object_name = 'list'


class UserDelete(DeleteView):
    model = User
    template_name = 'confirm_delete.html'
    success_url = '/colleges'


class Qpaper(CreateView):
    template_name = 'question.html'
    model = QuestionPaper
    form_class = QuestionSubForm
    success_url = '/addpaper'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['college'].queryset = form.fields['college'].queryset.filter(is_superuser=False)
        return form


class Pdflist(View):
    template_name = 'listquestions.html'
    model = QuestionPaper

    def get(self, request):
        current_time = datetime.now().time()
        specific_time = datetime.strptime("09:45:00", "%H:%M:%S").time()  # Specify the desired time here

        reply = QuestionPaper.objects.filter(college=request.user)
        context = {'list': reply, 'is_download_allowed': current_time >= specific_time}
        return render(request, self.template_name, context)


def generate_pdf(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Python Programming',
        difficulty='Simple'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def generate_pdf2(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Python Programming',
        difficulty='Medium'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def generate_pdf3(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Python Programming',
        difficulty='Difficult'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


class Subjectupdate(UpdateView):
    model = Subject
    template_name = 'question.html'
    fields = ['subject_name', 'semesters']
    success_url = '/subjects'


class SubjectDelete(DeleteView):
    template_name = 'confirm_delete.html'
    model = Subject
    success_url = '/subjects'


class Questupdate(UpdateView):
    model = Question
    template_name = 'question.html'
    fields = ['subjects', 'difficulty', 'questions']
    success_url = '/questionlist'


class QuestDelete(DeleteView):
    template_name = 'confirm_delete.html'
    model = Question
    success_url = '/questionlist'


def questionlist(request):
    products = list(Question.objects.all())

    return render(request, 'questionlist.html', {'products': products})


class SearchView(ListView):
    model = Question
    template_name = 'questionlist.html'
    context_object_name = 'products'

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            postresult = Question.objects.filter(subjects__subject_name__contains=query) | Question.objects.filter(
                questions__contains=query)
            result = postresult
        else:
            result = None
        return result


class Qngen(ListView):
    template_name = 'qngen.html'
    model = Subject
    context_object_name = 'list'


def math(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Computational Mathematics',
        difficulty='Simple'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def math2(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Computational Mathematics',
        difficulty='Medium'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def math3(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Computational Mathematics',
        difficulty='Difficult'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def web(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Advanced Web Technology',
        difficulty='Simple'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def web2(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Advanced Web Technology',
        difficulty='Medium'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def web3(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Advanced Web Technology',
        difficulty='Difficult'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def os(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Operating System',
        difficulty='Simple'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def os2(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Operating System',
        difficulty='Medium'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def os3(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Operating System',
        difficulty='Difficult'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def java(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Advanced Java Programming',
        difficulty='Simple'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def java2(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Advanced Java Programming',
        difficulty='Medium'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def java3(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Advanced Java Programming',
        difficulty='Difficult'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def ds(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Data Structure',
        difficulty='Simple'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def ds2(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Data Structure',
        difficulty='Medium'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def ds3(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Data Structure',
        difficulty='Difficult'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def network(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Computer Networks',
        difficulty='Simple'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def network2(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Computer Networks',
        difficulty='Medium'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def network3(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Computer Networks',
        difficulty='Difficult'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def Methodology(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Research Methodology',
        difficulty='Simple'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def Methodology2(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Research Methodology',
        difficulty='Medium'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def Methodology3(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Research Methodology',
        difficulty='Difficult'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def sql(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Database Management System',
        difficulty='Simple'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def sql2(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Database Management System',
        difficulty='Medium'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def sql3(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Database Management System',
        difficulty='Difficult'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def digital(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Digital Electronics and Computer Organisation',
        difficulty='Simple'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def digital2(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Digital Electronics and Computer Organisation',
        difficulty='Medium'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def digital3(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Digital Electronics and Computer Organisation',
        difficulty='Difficult'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def sw(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Software Engineering ',
        difficulty='Simple'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def sw2(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Software Engineering ',
        difficulty='Medium'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def sw3(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Software Engineering ',
        difficulty='Difficult'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def mining(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Data Mining',
        difficulty='Simple'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def mining2(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Data Mining',
        difficulty='Medium'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def mining3(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Data Mining',
        difficulty='Difficult'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def finance(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Finance',
        difficulty='Simple'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response

def finance2(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Finance',
        difficulty='Medium'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def finance3(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Finance',
        difficulty='Difficult'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response

def marketing(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Marketing',
        difficulty='Simple'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def marketing2(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Marketing',
        difficulty='Medium'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def marketing3(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Marketing',
        difficulty='Difficult'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response

def account(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Accounting',
        difficulty='Simple'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def account2(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Accounting',
        difficulty='Medium'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def account3(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Accounting',
        difficulty='Difficult'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response

def stati(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Statistics',
        difficulty='Simple'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def stati2(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Statistics',
        difficulty='Medium'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def stati3(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Statistics',
        difficulty='Difficult'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def business(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Business',
        difficulty='Simple'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def business2(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Business',
        difficulty='Medium'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def business3(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Business',
        difficulty='Difficult'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response

def tally(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Tally',
        difficulty='Simple'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def tally2(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Tally',
        difficulty='Medium'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def tally3(request):
    questions = Question.objects.filter(
        subjects__subject_name__contains='Tally',
        difficulty='Difficult'
    ).select_related('subjects')
    questions = random.sample(list(questions), 15)

    # Add subject semesters to question objects
    for question in questions:
        question.semesters = question.subjects.semesters

    # Set course name variable
    coursename = questions[0].subjects.course_name

    # Rendered
    html_string = render_to_string('generator.html', {'questions': questions, 'coursename': coursename})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=question.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response