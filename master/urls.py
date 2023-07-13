from django.urls import path,include
from .views import QuestionC, qlist, generate_pdf, Courcec, Signup, Login, Profile, Qpaper, Pdflist, generate_pdf2, \
    generate_pdf3, Home, SubjectDelete, Subjectupdate, questionlist, Questupdate, QuestDelete, SearchView, Qngen, math, \
    math2, math3, web, web2, web3, os, os2, os3, java, java2, java3, ds, ds2, ds3, network2, network3, network, mining, \
    mining2, mining3, Methodology, Methodology2, Methodology3, sw, sql, sql2, sql3, sw2, sw3, digital, digital2, \
    digital3, About, NewFeedbackView, ProfileUpdate, Feedbacks, Colleges, UserDelete,Coursecreation,Courseview,\
        CourseDetailView,create_course,Subjectview,SubjectDetailView,create_question,Error,finance,finance2,finance3, \
            marketing,marketing2,marketing3,account,account2,account3,business,business2,business3,stati,stati2,stati3, \
            tally,tally2,tally3
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.auth import views as auth_views

urlpatterns = [
                  path('addqn', QuestionC.as_view(), name='addqn'),
                  path('subjects', qlist, name='subjects'),
                  path('generate_pdf', generate_pdf, name='generate_pdf'),
                  path('generate_pdf2', generate_pdf2, name='generate_pdf2'),
                  path('generate_pdf3', generate_pdf3, name='generate_pdf3'),
                  path('addcourse', Courcec.as_view(), name='addcourse'),

                  path('createcourse', Coursecreation.as_view(), name='createcourse'),
                  path('viewcourse/', Courseview.as_view(), name='viewcourse'),
                  path('course_detail/(?p<pk>[0-9]+)', CourseDetailView.as_view(), name='course_detail'),
                  path('course_detail/<int:course_id>/subject_create/', create_course, name='create-course'),

                  path('viewsubject/', Subjectview.as_view(), name='viewsubject'),
                  path('subject_detail/(?p<pk>[0-9]+)', SubjectDetailView.as_view(), name='subject_detail'),
                   path('subject_detail/<int:subject_id>/question_create/', create_question, name='create-question'),
                   path('404', Error.as_view(), name='404'),
                   
                  path('home', Home.as_view(), name='home'),
                  path('', Home.as_view(), name=''),
                  path('about', About.as_view(), name='about'),
                  path('contact/', NewFeedbackView.as_view(), name='contact'),
                  path(r'signup/', Signup.as_view(), name='signup'),
                  path(r'login/', Login.as_view(), name='login'),
                  path(r'logout/', auth_views.LogoutView.as_view(), name='logout'),
                  path(r'profile/', Profile.as_view(), name='profile'),
                  path('proedit/(?p<pk>[0-9]+)', ProfileUpdate.as_view(), name='proedit'),

                  path(r'addpaper/', Qpaper.as_view(), name='addpaper'),
                  path(r'viewqstn/', Pdflist.as_view(), name='viewqstn'),
                  path('subup/(?p<pk>[0-9]+)', Subjectupdate.as_view(), name='subup'),
                  path('subdel/(?p<pk>[0-9]+)', SubjectDelete.as_view(), name='subdel'),

                  path(r'questionlist/', questionlist, name='questionlist'),
                  path('quesup/(?p<pk>[0-9]+)', Questupdate.as_view(), name='quesup'),
                  path('quesdel/(?p<pk>[0-9]+)', QuestDelete.as_view(), name='quesdel'),
                  path('search/', SearchView.as_view(), name='search'),
                  path('qngen/', Qngen.as_view(), name='qngen'),
                  path('colleges/', Colleges.as_view(), name='colleges'),
                  path('feedback/', Feedbacks.as_view(), name='feedback'),
                  path('userdel/(?p<pk>[0-9]+)', UserDelete.as_view(), name='userdel'),

                  path('maths2', math2, name='maths2'),
                  path('maths', math, name='maths'),
                  path('maths3', math3, name='maths3'),
                  path('web', web, name='web'),
                  path('web2', web2, name='web2'),
                  path('web3', web3, name='web3'),
                  path('os', os, name='os'),
                  path('os2', os2, name='os2'),
                  path('os3', os3, name='os3'),
                  path('java', java, name='java'),
                  path('java2', java2, name='java2'),
                  path('java3', java3, name='java3'),
                  path('ds', ds, name='ds'),
                  path('ds2', ds2, name='ds2'),
                  path('ds3', ds3, name='ds3'),
                  path('network', network, name='network'),
                  path('network2', network2, name='network2'),
                  path('network3', network3, name='network3'),
                  path('Methodology', Methodology, name='Methodology'),
                  path('Methodology2', Methodology2, name='Methodology2'),
                  path('Methodology3', Methodology3, name='Methodology3'),
                  path('sql', sql, name='sql'),
                  path('sql2', sql2, name='sql2'),
                  path('sql3', sql3, name='sql3'),
                  path('digital', digital, name='digital'),
                  path('digital2', digital2, name='digital2'),
                  path('digital3', digital3, name='digital3'),
                  path('sw', sw, name='sw'),
                  path('sw2', sw2, name='sw2'),
                  path('sw3', sw3, name='sw3'),
                  path('mining', mining, name='mining'),
                  path('mining2', mining2, name='mining2'),
                  path('mining3', mining3, name='mining3'),
                  path('tally', tally, name='tally'),path('tally2', tally2, name='tally2'),path('tally3', tally3, name='tally3'),
                  path('stati', stati, name='stati'),path('stati2', stati2, name='stati2'),path('stati3', stati3, name='stati3'),
                  path('business', business, name='business'),path('business2', business2, name='business2'),path('business3', business3, name='business3'),
                  path('finance', finance, name='finance'), path('finance2', finance2, name='finance2'), path('finance3', finance3, name='finance3'),
                  path('marketing', marketing, name='marketing'),path('marketing2', marketing2, name='marketing2'),path('marketing3', marketing3, name='marketing3'),
                  path('account', account, name='account'), path('account2', account2, name='account2'), path('account3', account3, name='account3'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
