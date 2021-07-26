from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from cities_light.models import Country, Region, City


from CATALOG.models import School, User, SchoolYear
from CATALOG.forms import SearchForm, NewSchoolForm, NewSchoolYearForm
from CATALOG.decorators import allowed_users


@login_required(login_url='/CATALOG/login/')
@allowed_users(allowed_types=['admin'])
def admin_schools(request):
    current_user = request.user

    schools = School.objects.all()

    form = SearchForm(auto_id=False)
    if request.method == 'POST':
        if 'search-submit' in request.POST:
            form = SearchForm(request.POST)
            if form.is_valid():
                school_name = form.cleaned_data['text']
                aux = schools
                schools = []
                for x in aux:
                    if school_name.lower() in str(x.name).lower():
                        schools.append(x)


    template = loader.get_template('CATALOG/Admin/Schools.html')

    context = {
        "schools": schools,
        'form': form,
        'user': current_user,
    }

    return HttpResponse(template.render(context, request))


@login_required(login_url='/CATALOG/login/')
@allowed_users(allowed_types=['admin'])
def admin_add_new_school(request):

    initial = {'school_year': SchoolYear.objects.latest('semester_1_start_date')}

    if request.method == 'GET':
        if request.is_ajax():
            if 'country_choice' in request.GET:
                print(request.GET.get('country_choice'))
                choice = request.GET.get('country_choice')
                country = Country.objects.filter(name=choice)[0];
                regions = Region.objects.filter(country_id=country.id)
                region_names = list()

                for region in regions:
                    region_names.append(region.name)

                return JsonResponse({'regions': region_names}, status=200)
            elif 'region_choice' in request.GET:
                choice = request.GET.get('region_choice')
                region = Region.objects.filter(name=choice)[0];
                cities = City.objects.filter(region_id=region.id)
                city_names = list()

                for city in cities:
                    city_names.append(city.name)

                return JsonResponse({'cities': city_names}, status=200)

    elif request.method == 'POST':
        form = NewSchoolForm(request.POST, initial=initial)
        if form.is_valid():
            result = form.create_school()

            if result is not None:
                messages.error(request, result)
                return redirect('/CATALOG/admin/new-school/')

            return redirect('/CATALOG/admin/schools/')

    template = loader.get_template('CATALOG/Admin/New-School.html')
    form = NewSchoolForm(initial=initial)

    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))
    

def admin_school_years(request):
    form = SearchForm()
    school_years = SchoolYear.objects.all()

    if request.method == 'POST':
        if 'search-submit' in request.POST:
            form = SearchForm(request.POST)
            text = form.cleaned_data['text']

            data = school_years
            school_years = []

            for school_year in data:
                if text.lower() in str(school_year).lower():
                    school_years.append(school_year)

    template = loader.get_template('CATALOG/Admin/School-Years.html')
    context = {
        'school_years': school_years,
        'form': form,
    }

    return HttpResponse(template.render(context, request))

def admin_add_new_school_year(request):
    template = loader.get_template('CATALOG/Admin/New-School-Year.html')

    form = NewSchoolYearForm()

    if request.method == 'POST':
        form = NewSchoolYearForm(request.POST)
        if form.is_valid():
            result = form.create_school_year()

            if result is not None:
                messages.error(request, result)
                return redirect('/CATALOG/admin/new-school-year/')
            else: 
                return redirect('/CATALOG/admin/school-years/')

    context = {
        'form': form,
    }

    return HttpResponse(template.render(context, request))