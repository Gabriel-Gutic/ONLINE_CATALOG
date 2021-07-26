from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect


from CATALOG.models import Teacher, School, Class
from CATALOG.forms import SearchForm, NewTeacherForm, NewClassForm, ExistingUserForm
from CATALOG.decorators import allowed_users


@login_required(login_url='/CATALOG/login/')
@allowed_users(allowed_types=['school-admin'])
def school_teachers(request):
    
    form = SearchForm(auto_id=False)

    teachers = Teacher.objects.filter(schools=School.objects.get(user=request.user))
    if request.method == 'POST':
        if 'search-submit' in request.POST:
            form = SearchForm(request.POST)
            if form.is_valid():
                data = teachers
                teachers = []
                text = str(form.cleaned_data['text']).lower()

                #select teachers whose names contains text
                for teacher in data:
                    if text in (str(teacher).lower()):
                        teachers.append(teacher)
    
    template = loader.get_template('CATALOG/School/Teachers.html')

    context = {
        'teachers': teachers,
        'form': form,
    }

    return HttpResponse(template.render(context, request))


@login_required(login_url='/CATALOG/login/')
@allowed_users(allowed_types=['school-admin'])
def school_add_new_teacher(request):
    form = NewTeacherForm()

    if request.method == 'POST':
        if 'add-new-teacher-submit' in request.POST:
            form = NewTeacherForm(request.POST)
            if form.is_valid():

                result = form.create_teacher(school=School.objects.get(user=request.user))

                if result is not None:
                    messages.error(request, result)
                    return redirect('/CATALOG/school/new-teacher/')
                else:
                    return redirect('/CATALOG/school/teachers/')

    template = loader.get_template('CATALOG/School/New-Teacher.html')
    context = {
        'form': form,
    }

    return HttpResponse(template.render(context, request))


@login_required(login_url='/CATALOG/login/')
@allowed_users(allowed_types=['school-admin'])
def school_add_existing_teacher(request):

    form = ExistingUserForm()

    if request.method == 'POST':
        form = ExistingUserForm(request.POST)
        if form.is_valid():

            result = form.get_user(type=3)

            if result['error'] == True:
                messages.error(request, result['value'])
                return redirect('/CATALOG/school/existing-teacher/')
            
            existing_user = result['value']
            teacher = Teacher.objects.get(user=existing_user)
            school = School.objects.get(user=request.user)
            if school in teacher.schools.all():
                messages.error(request, 'Teacher is already in this school!')
                return redirect('/CATALOG/school/existing-teacher/')

            teacher.schools.add(school)
            return redirect('/CATALOG/school/teachers/')

    template = loader.get_template('CATALOG/School/Existing-Teacher.html')
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))


def school_classes(request):

    form = SearchForm()
    classes = Class.objects.filter(school=School.objects.get(user=request.user))

    if request.method == 'POST':
        if 'search-submit' in request.POST:
            form =  SearchForm(request.POST)
            if form.is_valid():
                data =  classes
                classes = []
    
                text = str(form.cleaned_data['text']).lower()
    
                for _class in data:
                    if text in str(_class.name).lower():
                        classes.append(_class)

    template = loader.get_template('CATALOG/School/Classes.html')
    context = {
        'form': form,
        'classes': classes,
    }

    return HttpResponse(template.render(context, request))
    

def school_add_new_class(request):
    
    form = NewClassForm()

    if request.method == 'POST':
        form = NewClassForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['number']
            type = form.cleaned_data['type']
            school = School.objects.get(user=request.user)
            new_class = Class.objects.create(number=number, type=type, school=school)
            new_class.save()
            return redirect('/CATALOG/school/classes/')

    template = loader.get_template('CATALOG/School/New-Class.html')
    context = {
        'form': form,
    }

    return HttpResponse(template.render(context, request))