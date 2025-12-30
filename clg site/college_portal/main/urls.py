from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('syllabus/', views.syllabus, name='syllabus'),
    path('timetable/', views.timetable, name='timetable'),
    path("pa_lab/", views.pa_lab, name="pa_lab"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("pa-lab/exp1/", views.exp1, name="exp1"),
    path("pa-lab/exp2/", views.exp2, name="exp2"),
    path("pa-lab/exp3/", views.exp3, name="exp3"),
    path("pa-lab/exp4/", views.exp4, name="exp4"),
    path("pa-lab/exp5/", views.exp5, name="exp5"),
    path("pa-lab/exp6/", views.exp6, name="exp6"),
    path("pa-lab/exp7/", views.exp7, name="exp7"),
    path("pa-lab/exp8/", views.exp8, name="exp8"),
    path("pa-lab/exp9/", views.exp9, name="exp9"),
    path("pa-lab/exp10/", views.exp10, name="exp10"),
    path("pa-lab/exp11/", views.exp11, name="exp11"),
    path('lecturer/login/', views.lecturer_login, name='lecturer_login'),
    path('lecturer/register/', views.lecturer_register, name='lecturer_register'),
    path('lab/delete-session/', views.delete_session, name='delete_session'),
    path('lab/marks/', views.lab_marks, name='lab_marks'),
    path('lab/add-session/', views.add_session, name='add_session'),
    path('lab/save-mark/', views.save_mark, name='save_mark'),
    path('lab/pdf/', views.download_lab_pdf, name='download_lab_pdf'),

]
