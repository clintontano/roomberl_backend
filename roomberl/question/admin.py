from core.admin import ImportExportModelAdmin
from django.contrib import admin
from question.models import Category
from question.models import Option
from question.models import Question

# Register your models here.


class OptionInline(admin.TabularInline):
    model = Option


class QuestionInline(admin.TabularInline):
    model = Question


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    list_display = ["text", "category"]
    inlines = [OptionInline]


@admin.register(Option)
class OptionAdmin(ImportExportModelAdmin):
    pass
