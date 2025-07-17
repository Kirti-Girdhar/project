from django.urls import path
from . import views

urlpatterns=[
    path('showform/',views.showform),
    path('viewquestion/',views.viewquestion),
    path('addquestion/',views.AddQuestion),
    path('updatequestion/',views.UpdateQuestion),
    path('deletequestion/',views.DeleteQuestion),
    path('givemelogin/',views.giveMeLogin),
    path('givemeregistration/',views.giveMeRegistration),
    path('register/',views.register),
    path('login/',views.login),
    path('nextquestion/',views.nextQuestion),
    path('givemesubject/', views.giveMesubject),
    path('givemequestion/', views.giveMeQuestion),
    path('startTest/',views.startTest),
    path('previousquestion/',views.previousQuestion),
    path("endexam/",views.endexam),
    path("senddata/",views.sendData),
    path('getuser/<uname>',views.getUser),
    path('getuser2/<uname>',views.getUser2),
    path('adduser/',views.addUser),
    path('updateuser/',views.updateUser),
    path('deleteuser/<uname>',views.deleteUser),
    path('getalluser/',views.getAllUser)
]
