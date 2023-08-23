from django.urls import path, include
from app.api import question_views, stage_views

from django.contrib import admin

urlpatterns = [

    path('get-question/', question_views.GetQuestionApiView.as_view()),
    path('question-lists/<slug:slug>/',stage_views.StageQuestionViewSet.as_view({'get':'list'})),
    path('question-lists/<slug:slug>/<int:pk>/',stage_views.StageQuestionViewSet.as_view({'get':'retrieve'})),
    path('add-stage-question/', question_views.AddQuestionApiView.as_view()),
    ###
    
    path('stage-object/<slug:slug>/',stage_views.StageObjectApiView.as_view()),
    path('stage-parent-lists/', stage_views.StageParentListApiView.as_view(), name = 'parent-stage-api'),
    path('stage-child-lists/', stage_views.StageChildListApiView.as_view(), name = 'child-stage-api'),



]
