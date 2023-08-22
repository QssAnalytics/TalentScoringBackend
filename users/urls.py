from django.urls import path, include


from django.contrib import admin

from users.api import repot_views, user_views
urlpatterns = [
    path('login/', user_views.loginView),
    path('register/', user_views.registerView),
    path('refresh-token/', user_views.CookieTokenRefreshView.as_view()),
    path('logout/', user_views.logoutView),
    path('user/', user_views.user),
    path('user-education-score/<str:username>/', user_views.UserScoreAPIView.as_view()),
    path('get-summry-prompt/', user_views.SummryPromptAPIView.as_view()),
    path('get-experiance-prompt/', user_views.ExperiancePromptAPIView.as_view()),
    path('get-job-title-prompt/', user_views.JobTitleAPIView.as_view()),
    path('user-info-post/', user_views.UserInfoPost.as_view()),
    path('upload-report/', repot_views.ReportUploadAPIView.as_view()),
    path('get-report/', repot_views.ReportInfoAPIView.as_view()),
    path('get-input/', user_views.InputAPIView.as_view()), ####
    path('get-certificate-intro/', user_views.CertificateIntroAPIView.as_view()) ####

]