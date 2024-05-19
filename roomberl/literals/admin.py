from django.contrib import admin
from literals.models import Hostel
from literals.models import RoomType
from literals.models import Semester
from literals.models import University
from literals.models import Year

# Register your models here.


admin.site.site_header = "ROOMBRL ADMINISTRATOR"
admin.site.site_title = "ROOMBRL PORTAL"
admin.site.index_title = "ROOMBRL  ADMINISTRATOR PORTAL"

admin.site.register([University, RoomType, Hostel, Semester, Year])
