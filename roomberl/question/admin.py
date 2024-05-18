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
class CategoryAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["text", "category"]
    inlines = [OptionInline]
