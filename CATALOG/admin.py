from django.contrib import admin

from . import models


admin.site.register(models.User)

admin.site.register(models.SchoolYear)
admin.site.register(models.School)
admin.site.register(models.Class)
admin.site.register(models.Student)
admin.site.register(models.StudentArchive)
admin.site.register(models.Teacher)
admin.site.register(models.Subject)
admin.site.register(models.Schedule)
admin.site.register(models.Note)