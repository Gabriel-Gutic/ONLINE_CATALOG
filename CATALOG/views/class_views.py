from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.shortcuts import redirect

from CATALOG.models import Class, Student, StudentArchive
from CATALOG.forms import SearchForm, NewStudentForm, ExistingUserForm


def class_page_url(class_id):
    return '/CATALOG/school/classes/' + str(class_id) + '/'


def class_students(request, class_id):
    _class = Class.objects.get(id=class_id)
    student_archives = StudentArchive.objects.filter(class_id=_class)
    students = []
    for archive in student_archives:
        if archive.end_date is None:
            students.append(archive.student)

    form = SearchForm()

    template = loader.get_template('CATALOG/School/Class/Students.html')
    context = {
        'class': _class,
        'form': form,
        'students': students,
    }
    return HttpResponse(template.render(context, request))


def class_add_new_student(request, class_id):
    form = NewStudentForm()

    if request.method == 'POST':
        form = NewStudentForm(request.POST)

        if form.is_valid():
            result = form.create_student(class_id=class_id)
            if result is not None:
                messages.error(request, result)
                return redirect(class_page_url(class_id=class_id) + 'new-student/')
            return redirect(class_page_url(class_id=class_id))

    template = loader.get_template('CATALOG/School/Class/New-Student.html')
    context = {
        'form': form,
    }

    return HttpResponse(template.render(context, request))


def class_add_existing_student(request, class_id):
    form = ExistingUserForm()

    if request.method == 'POST':
        form = ExistingUserForm(request.POST)
        if form.is_valid():
            result = form.create_user(type=4)

            if result['error'] == True:
                messages.error(request, result['value'])
                return redirect(class_page_url(class_id=class_id) + 'existing-student/')
            
