from django.urls import path
from client import views
from django.conf import settings
from django.conf.urls.static import static

app_name="client"
urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.SignUpPage, name='register'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
