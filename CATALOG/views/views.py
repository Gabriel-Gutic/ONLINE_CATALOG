from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


from CATALOG.forms import LoginForm
from CATALOG.models import School, Teacher, Student


def home_page(request):
    template = loader.get_template('CATALOG/Home.html')
    return HttpResponse(template.render({}, request))


def not_permission_page(request):
    template = loader.get_template('CATALOG/Not-Permission.html')
    return HttpResponse(template.render({}, request))


#TODO profile picture update

@csrf_exempt
@login_required(login_url='/CATALOG/login/')
def profile_page(request):

    user = request.user
    if request.method == 'POST':

        #Modify user's profile picture
        if "image" in request.FILES:
            img = request.FILES.get('image')

            extensions = ["jpg", "png",  "gif", "bmp"]
            list = img.name.split(".")
            extension = list[-1]
            if not extension in extensions:
                messages.error(request,'Not a valid image!')
                return redirect('/CATALOG/profile/')
            
            user.image = img;
            user.save()
            print("User's profile picture modified!")

    context = {
        'user': user,
    }
    if user.type == 1:
        template = loader.get_template('CATALOG/Users/Profile/Admin-Profile.html')
    elif user.type == 2:
        template = loader.get_template('CATALOG/Users/Profile/School-Admin-Profile.html')
        school = School.objects.get(USER=user)
        context['school'] = school
    elif user.type == 3:
        teacher = Teacher.objects.get(USER=user)
        context['teacher'] = teacher
    else:
        student = Student.objects.get(USER=user)
        context['student'] = student
    
    return HttpResponse(template.render(context, request))


def login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                remember_me = request.POST.get('remember_me')
                if  not remember_me:
                    request.session.set_expiry(7200)
                    request.session.modified = True
                else:
                    request.session.set_expiry(None)
                    request.session.modified = True
                next = request.GET.get('next')
                if next == "/CATALOG/logout/" or next == None:
                    return redirect("/CATALOG/home/")
                return HttpResponseRedirect(next)
        else:
            messages.error(request,'Username or password not correct!')
            return redirect('/CATALOG/login/')
    else:
        form = LoginForm()

    template = loader.get_template('CATALOG/Users/login.html')
    context = {'form': form,}
    return HttpResponse(template.render(context, request))


def school_admin_interface(request):
    pass


def teacher_interface(request):
    pass


def student_interface(request):
    pass
