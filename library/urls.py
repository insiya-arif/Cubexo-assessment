from django.urls import path
from library import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.landing, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('reading-list/', views.reading_list, name='reading_list'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
]