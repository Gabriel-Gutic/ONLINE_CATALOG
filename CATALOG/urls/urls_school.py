from CATALOG.views import school_views
from django.urls import path, include


urlpatterns = [
    path('teachers/', school_views.school_teachers, name='school-teachers'),
    path('new-teacher/', school_views.school_add_new_teacher, name='school_add_new_teacher'),
    path('existing-teacher/', school_views.school_add_existing_teacher, name='school_add_existing_teacher'),
    path('classes/', include('CATALOG.urls.urls_class')),
    path('new-class/', school_views.school_add_new_class, name='school_add_new_class'),
]
