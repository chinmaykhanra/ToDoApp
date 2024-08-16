from django.urls import path
from myapp import views

app_name = 'task'

urlpatterns = [
	path('', views.index, name="index"),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.handlelogin, name='handlelogin'),
    path('logout/', views.handlelogout, name='handlelogout'),
    path('addtask', views.addTask, name="addtask"),
    path('editTask/<int:task_id>/', views.editTask, name='editTask'),
    path('completeTask/<int:task_id>/', views.completeTask, name='completeTask'),
    path('calender', views.calender, name='calender'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('request-reset-email/',views.RequestResetEmailView.as_view(),name='request-reset-email'),
    path('set-new-password/<uidb64>/<token>',views.SetNewPasswordView.as_view(),name='set-new-password'),
]