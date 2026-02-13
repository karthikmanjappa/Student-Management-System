from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('profile/', views.profile_dashboard, name='profile_dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),



    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),

    

    path('logout/', views.user_logout, name='logout'),
    path("course/", views.course_page, name="course_page"),


]
