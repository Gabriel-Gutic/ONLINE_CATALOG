from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as gtl
from django.shortcuts import get_object_or_404
from cities_light.models import City

class AccountManager(BaseUserManager):

    def create_user(self, email, user_name, password, **other_fields):
        
        if not email:
            raise ValueError(gtl("Please provide an email address"))

        other_fields.setdefault('is_active', True)
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)

        user.set_password(password)

        type = other_fields.get('type')
        
        user.save()
        
        if type == 2:
            group = get_object_or_404(Group, name='school-admin-group')
            user.groups.add(group.id)
        elif type == 3:
            group = get_object_or_404(Group, name='teacher-group')
            user.groups.add(group.id)
        elif type == 4:
            group = get_object_or_404(Group, name='student-group')
            user.groups.add(group.id)

        user.save()

        return user

    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault('type', 1)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(gtl("Superuser must be asssigned to is_staff=True"))

        if other_fields.get('is_superuser') is not True:
            raise ValueError(gtl("Superuser must be asssigned to is_superuser=True"))

        return self.create_user(email, user_name, password, **other_fields)

USER_TYPE_CHOICES = (
      (1, 'admin'),
      (2, 'school-admin'),
      (3, 'teacher'),
      (4, 'student'),
    )

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    user_name = models.CharField(max_length=200, unique=True)
    start_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'type']

    def __str__(self):
        return self.user_name


class SchoolYear(models.Model):
    semester_1_start_date = models.DateField()
    semester_1_end_date = models.DateField()
    semester_2_start_date = models.DateField()
    semester_2_end_date = models.DateField()

    def __str__(self):
        return str(self.semester_1_start_date.year) + '-' + str(self.semester_2_end_date.year)


class School(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=20, null=True, blank=True) 
    year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class Class(models.Model):
    id = models.BigAutoField(primary_key = True)
    number = models.IntegerField(default=1)
    type = models.CharField(max_length=20, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    class Meta:
        db_table = 'class'
        # Add verbose name
        verbose_name = 'Classe'

    def __str__(self):
        if self.type is not None:
            return str(self.number) + ' ' + str(self.type) + ' --- ' + self.school.user.user_name
        return str(self.number) + ' --- ' + self.school.user.user_name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    birthdate = models.DateField()
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.last_name + ' ' + self.first_name


class StudentArchive(models.Model):
    id = models.BigAutoField(primary_key = True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        student = Student.objects.get(user=self.student)

        if self.class_id.type is not None:
            return student.last_name + ' ' + student.first_name + ' --- ' + str(self.class_id.number) + ' ' + str(self.class_id.type)
        return student.last_name + ' ' + student.first_name + ' --- ' + str(self.class_id.number)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    birthdate = models.DateField()
    phone = models.CharField(max_length=20, null=True, blank=True)
    schools = models.ManyToManyField(School, blank=True)

    def __str__(self):
        return self.last_name + ' ' + self.first_name


class Subject(models.Model):
    id = models.BigAutoField(primary_key = True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.ID)


class Schedule(models.Model):
    id = models.BigAutoField(primary_key = True)

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="CLASS_related")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="SUBJECT_related")

    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()

    def __str__(self):
        return str(self.ID)


DEFAULT = "DEFAULT"
YEARLY_AVERAGE = "YEARLY_AVERAGE"
HALF_YEARLY_AVERAGE = "HALF_YEARLY_AVERAGE"
THESIS = "THESIS"


NOTE_TYPES = (
    (DEFAULT, "DEFAULT"),
    (YEARLY_AVERAGE, "YEARLY_AVERAGE"),
    (HALF_YEARLY_AVERAGE, "HALF_YEARLY_AVERAGE"),
    (THESIS, "THESIS")
)


class Note(models.Model):
    id = models.BigAutoField(primary_key = True)
    value = models.FloatField()
    type = models.CharField(max_length=20, choices=NOTE_TYPES, default="DEFAULT")

    student_archive = models.ForeignKey(StudentArchive, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE,  null=True)

    def __str__(self):
        return str(self.ID)