from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views


urlpatterns = [
    path('members/', views.MemberList.as_view()),
    path('members/<int:pk>/', views.MemberByID.as_view()),
    path('members/account/<int:account_id>/', views.MemberByAccount.as_view()),
    path('members/phone/<phone_number>/', views.MemberByPhone.as_view()),
    path('members/client/<int:client_member_id>/', views.MemberByClient.as_view()),
    path('upload/', views.FileUploadView.as_view()),
    path('process/<filename>/', views.ProcessFile.as_view()),

]


urlpatterns = format_suffix_patterns(urlpatterns)