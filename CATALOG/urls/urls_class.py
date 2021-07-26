from django.urls import path

from CATALOG.views import school_views, class_views


urlpatterns = [
    path('', school_views.school_classes, name='school_classes'),
    path('<int:class_id>/', class_views.class_students, name='school_classes'),
    path('<int:class_id>/new-student/', class_views.class_add_new_student, name='school_classes'),
    path('<int:class_id>/existing-student/', class_views.class_add_existing_student, name='class_add_existing_student'),
]
