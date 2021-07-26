from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from cities_light.models import Country, Region, City


from .models import School, SchoolYear, Teacher, Student, StudentArchive, Class, User


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'remember-me'}))  # add the remember_me field


class SearchForm(forms.Form):
    text = forms.CharField(required=False, label="", widget=forms.TextInput(attrs={'class':'school-name-search'}), max_length=200)


class LocationModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class ExistingUserForm(forms.Form):
    field = forms.CharField(label="Username/Email", max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))

    def get_user(self, type):
        try:
            user = User.objects.get(user_name=self.cleaned_data['field'])
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=self.cleaned_data['field'])
            except User.DoesNotExist:
                return {
                    'error': True,
                    'value': 'User does not exist!'
                }

        if user.type != type:
            return {
                    'error': True,
                    'value': 'Invalid user!'
                }

        return {
            'error': False,
            'value': user,
            }


class NewSchoolYearForm(forms.Form):
    semester_1_start_date =  forms.DateField(label="Semester 1 start date", widget=forms.DateInput(attrs={'class':'form-control datepicker'}))
    semester_1_end_date =  forms.DateField(label="Semester 1 end date", widget=forms.DateInput(attrs={'class':'form-control datepicker'}))
    semester_2_start_date =  forms.DateField(label="Semester 2 start date", widget=forms.DateInput(attrs={'class':'form-control datepicker'}))
    semester_2_end_date =  forms.DateField(label="Semester 2 end date", widget=forms.DateInput(attrs={'class':'form-control datepicker'}))

    def create_school_year(self):
        semester_1_start_date = self.cleaned_data['semester_1_start_date']
        semester_1_end_date = self.cleaned_data['semester_1_end_date']
        semester_2_start_date = self.cleaned_data['semester_2_start_date']
        semester_2_end_date = self.cleaned_data['semester_2_end_date']

        if semester_1_end_date > semester_2_start_date or semester_1_start_date > semester_1_end_date or semester_2_start_date > semester_2_end_date:
            return "Invalid data!"

        school_year = SchoolYear.objects.create(
            semester_1_start_date=semester_1_start_date,
            semester_1_end_date=semester_1_end_date,
            semester_2_start_date=semester_2_start_date,
            semester_2_end_date=semester_2_end_date,
        )
        school_year.save()

        return None


#TODO: abstract user form
class NewUserForm(forms.Form):
    username =  forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(required = False, label="Email", max_length=200, widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'password-field'}))
    password_again = forms.CharField(label="Password(again)", max_length=50, widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'password-again-field'}))

    def __valid_username(self, username):
        for c in str(username):
            if not c.isalnum() and c != '_':
                return False
        return True

    def _get_type(self):
        return 4

    def _create_user(self):
        error = 'error'

        USERNAME = self.cleaned_data['username']

        USERNAME =  str(USERNAME).rstrip()

        result = self.__valid_username(USERNAME)
        if result is False:
            return [error, "Username must contains only letters, numbers and '_'!"]

        try:
            object = User.objects.get(user_name=USERNAME)
        except User.DoesNotExist:
            object = None
        if object is not None:
            return [error, 'Username already used!']


        EMAIL = self.cleaned_data['email']

        try:
            object = User.objects.get(email=EMAIL)
        except User.DoesNotExist:
            object = None
        if object is not None:
            return [error, 'Email already used!']

        PASSWORD = self.cleaned_data['password']
        PASSWORD_AGAIN = self.cleaned_data['password_again']

        if PASSWORD != PASSWORD_AGAIN:
                return [error, 'Passwords not match!']

        db = get_user_model()
        user = db.objects.create_user(
            user_name=USERNAME,
            email=EMAIL,
            password=PASSWORD,
            type=self._get_type(),
        )
        return [None, user]


class NewSchoolForm(NewUserForm):
    name = forms.CharField(label="Name", max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
    country = forms.ChoiceField(label="Country", widget=forms.Select(attrs={'id': 'country-select', 'class':'form-control'}), choices=[('', ' -- select an option -- ')] + [(name, name) for name in Country.objects.values_list('name', flat=True).distinct()])
    region = forms.ChoiceField(label="Region", widget=forms.Select(attrs={'id':'region-select', 'class':'form-control'}), choices=[('', ' -- select an option -- ')] + [(name, name) for name in Region.objects.values_list('name', flat=True).distinct()])  
    city = forms.ChoiceField(label="City", widget=forms.Select(attrs={'id':'city-select', 'class':'form-control'}), choices=[('', ' -- select an option -- ')] + [(name, name) for name in City.objects.values_list('name', flat=True).distinct()])   
    address = forms.CharField(label="Address", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    phone = forms.CharField(required = False, label="Phone(optional)", max_length=15, widget=forms.TextInput(attrs={'class':'form-control'}))
    school_year = forms.ModelChoiceField(label="School Year", queryset=SchoolYear.objects.all())

    def _get_type(self):
        return 2

    def create_school(self):

        result = self._create_user()

        if result[0] is not None:
            return result[1]
        
        NAME = self.cleaned_data['name']
        ADDRESS = self.cleaned_data['address']
        PHONE = self.cleaned_data['phone']
        YEAR = self.cleaned_data['school_year']
        COUNTRY = self.cleaned_data['country']

        country = Country.objects.filter(name=COUNTRY)[0]

        REGION = self.cleaned_data['region']
        region = Region.objects.filter(name=REGION, country_id=country.id)[0]

        CITY = self.cleaned_data['city']
        city = City.objects.filter(name=CITY, region_id=region.id)[0]

        school = School.objects.create(user=result[1], name=NAME, city=city, address=ADDRESS, phone=PHONE, year=YEAR)
        school.save()
        return None


class NewTeacherForm(NewUserForm):
    last_name = forms.CharField(label="Last Name", max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(label="First Name", max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
    birthdate = forms.DateField(label="Birthdate", widget=forms.DateInput(attrs={'class':'form-control datepicker'}))
    phone = forms.CharField(required = False, label="Phone(optional)", max_length=15, widget=forms.TextInput(attrs={'class':'form-control'}))

    def _get_type(self):
        return 3

    def create_teacher(self, school):
        
        result = self._create_user()

        if result[0] is not None:
            return result[1]

        user = result[1]

        LAST_NAME = self.cleaned_data['last_name']
        FIRST_NAME = self.cleaned_data['first_name']
        BIRTHDATE = self.cleaned_data['birthdate']
        PHONE = self.cleaned_data['phone']

        teacher = Teacher.objects.create(user=user, last_name=LAST_NAME, first_name=FIRST_NAME, birthdate=BIRTHDATE, phone=PHONE)
        teacher.save()
        teacher.schools.add(school)
        return None


class NewClassForm(forms.Form):
    number = forms.CharField(label="Number", max_length=200, widget=forms.TextInput(attrs={'id':'name-field', 'class':'form-control'}))
    type = forms.CharField(label="Type(optional)", required=False, max_length=200, widget=forms.TextInput(attrs={'id':'type-field', 'class':'form-control'}))

class NewStudentForm(NewUserForm):
    last_name = forms.CharField(label="Last Name", max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(label="First Name", max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
    birthdate = forms.DateField(label="Birthdate", widget=forms.DateInput(attrs={'class':'form-control datepicker'}))
    phone = forms.CharField(required = False, label="Phone(optional)", max_length=15, widget=forms.TextInput(attrs={'class':'form-control'}))
    
    def _get_type(self):
        return 4

    def create_student(self, class_id):
        result = self._create_user()

        if result[0] is not None:
            return result[1]

        user = result[1]

        LAST_NAME = self.cleaned_data['last_name']
        FIRST_NAME = self.cleaned_data['first_name']
        BIRTHDATE = self.cleaned_data['birthdate']
        PHONE = self.cleaned_data['phone']

        _class = Class.objects.get(id=class_id)

        student = Student.objects.create(user=user, last_name=LAST_NAME, first_name=FIRST_NAME, birthdate=BIRTHDATE, phone=PHONE)
        student.save()

        student_archive = StudentArchive.objects.create(student=student, class_id=_class)

        return None