from django.urls import path, re_path
from . import views

app_name = 'onlinecourses'

urlpatterns = [

    path('terms/', views.terms, name='terms'),
    path('courses/me', views.courses_me, name='courses_me'),
    path('courses/all', views.courses_all, name='courses_all'),
    path('courses/instructor/all', views.instructor_courses, name='instructor_courses_all'),
    path('courses/search/', views.search_courses, name='search_result'),   
    path('course/<int:pk>/', views.load_course, name = 'load_course'),
    path('course/student/<slug>/start/', views.student_start_course, name = 'student_start_course'),
    path('course/student/lesson/<slug>/start', views.student_start_lesson, name = 'student_start_lesson'),
    path('course/delete/<int:pk>/', views.delete_course, name = 'delete_course'),
    path('course/edit/<int:pk>/', views.edit_course, name = 'edit_course'),
    path('course/open/<int:pk>/', views.open_course, name = 'open_course'),
    path('course/buy/<slug>/', views.buy_course, name = 'buy_course'),
    path('course/review/add/<int:pk>/', views.add_comment, name = 'add_comment'),
    path('courses/create/', views.create_course, name='create_course'), 
    path('courses/addcategory/', views.AddCategory, name='add_category'), 
    path('course/lesson/add/', views.add_lesson, name='add_lesson'),
     path('course/lesson/add_more/<int:pk>/', views.add_more_lesson, name='add_more_lesson'),
    path('course/lesson/<int:pk>/preview/', views.instructor_lesson_preview, name='lesson_preview'),
    path('course/course/<int:pk>/preview/', views.instructor_course_preview, name='course_preview'),
    path('course/lesson/addtext/<int:id>', views.Add_Lesson_text, name='add_text'),
    
    
]