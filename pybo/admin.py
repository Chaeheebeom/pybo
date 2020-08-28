from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Question
#api문서 주소 https://docs.djangoproject.com/en/3.0/ref/contrib/admin/
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']

#장고관리자 화면에서 관리가 가능함.
admin.site.register(Question, QuestionAdmin)


