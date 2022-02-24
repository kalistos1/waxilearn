from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns=[
    path('signin/',views.SignIn, name="login"),
    path('signup/',views.SignUp, name="register"),
    path('signout/',views.signout, name="logout"),
    path('dashboard/instructorDashboard',views.InstructorDashboard, name="instructordashboard"),
    #path('dashboard/instructorDashboard/<int:pk>',views.InstructorDashboard, name="instructordashboardwithpk"),
    path('dashboard/studentDasboard/',views.StudentDashboard, name="studentdashboard"),
    #path('dashboard/instructorDashboard/profileedit/',views.InstructorProfileEdit, name="instructorprofileedit"),
    path('profile/student/edit', views.edit_profile, name='student_edit_profile'),
    path('profile/instructor/edit', views.edit_profile, name='instructor_edit_profile'),
    path('profile/instructor/profile', views.InstructorProfile, name='instructor_profile'),
    path('profile/user/<int:pk>/delete/', views.delete_user, name='delete_user'),
    path('profile/betsubscriber/<int:id>/delete/', views.delete_bet_subscriber, name='delete_bet_subscriber'),
    path('profile/signalsubscriber/<int:id>/delete/', views.delete_signal_subscriber, name='delete_signal_subscriber'),
    path('profile/learningsubscriber/<int:id>/delete/', views.delete_learning_subscriber, name='delete_learning_subscriber'),
    path('profile/photo/upload', views.upload_profile_photo, name='upload_profile_photo'),
    path('profile/login/edit', views.change_login_details, name='change_login_details'),
    path('profile/username/change/<int:pk>', views.change_username, name='change_username'),
    path('profile/password/change/<int:pk>', views.change_password, name='change_password'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name = 'accounts/password_reset.html'), name='password_reset' ),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name= 'accounts/password_reset_done.html'), name='password_reset_done' ),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name='password_reset_complete '),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('delete/student/sub_type/<int:pk>/',views.delete_student_sub_type, name="delete_student_sub_type"),
    path('delete/betting/sub_type/<int:pk>/',views.delete_betting_sub_type, name="delete_betting_sub_type"),
    path('delete/signal/sub_type/<int:pk>/',views.delete_signal_sub_type, name="delete_signal_sub_type"),
    path('edit/student/sub_type/<int:pk>/',views.edit_student_sub_type, name="edit_student_sub_type"),
    path('edit/betting/sub_type/<int:pk>/',views.edit_betting_sub_type, name="edit_betting_sub_type"),
    path('edit/signal/sub_type/<int:pk>/',views.edit_signal_sub_type, name="edit_signal_sub_type"),
]
