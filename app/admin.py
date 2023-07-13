from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from app import models as model
from django.contrib.admin.widgets import AutocompleteSelect
from django.db import models
# Register your models here.


class AnswerTabularInline(admin.TabularInline):
    model = model.Answer
    fields = ('answer_title', 'answer_weight', 'answer_dependens_on', 'stage_fit')
    raw_id_fields = ('answer_dependens_on', 'stage_fit')
    fk_name = "questionIdd"
    list_select_related = ['questionIdd', 'answer_dependens_on', 'stage_fit']

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).select_related('questionIdd')


@admin.register(model.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_title', 'stage', 'question_dependens_on_answer', 'question_type')
    inlines = [AnswerTabularInline]
    search_fields = ('question_title', 'question_dependens_on_question')
    list_select_related = ['stage', 'question_dependens_on_answer__stage_fit', 'question_dependens_on_answer__questionIdd']


@admin.register(model.Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('stage_name', 'parent', 'slug', 'stage_index')


@admin.register(model.Answer)
class AnswerAdmin(admin.ModelAdmin):
    search_fields= ('answer_title',)
    autocomplete_fields = ['answer_dependens_on']
    list_display = ('answer_title', 'question_title', 'answer_weight')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('questionIdd')
        return queryset

    def question_title(self, obj):
        return obj.questionIdd.question_title

    question_title.short_description = 'Question'


admin.site.register(model.UserAccount) 
