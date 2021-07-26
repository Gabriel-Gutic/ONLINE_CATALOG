from django.urls import path, include
from django.contrib.auth import views as authtentication_views

from CATALOG.views import views


urlpatterns = [
    path('home/', views.home_page, name='home_page'),
    path('teacher/', views.teacher_interface, name='teacher_interface'),
    path('admin/', include('CATALOG.urls.urls_admin')),
    path('school/', include('CATALOG.urls.urls_school')),
    path('login/', views.login, name='login'),
    path('logout/', authtentication_views.LogoutView.as_view(template_name='CATALOG/Users/logout.html'), name='logout'),
    path('not-permission/', views.not_permission_page, name='not_permission-page'),
    path('profile/', views.profile_page, name='profile-page'),
]