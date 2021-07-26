from django.urls import path, include

from CATALOG.views import admin_views


urlpatterns = [
    path('schools/', admin_views.admin_schools, name='admin_schools'),
    path('new-school/', admin_views.admin_add_new_school, name='admin_add_new_school'),
    path('school-years/', admin_views.admin_school_years, name='admin_school_years'),
    path('new-school-year/', admin_views.admin_add_new_school_year, name='admin_add_new_school_year'),
]