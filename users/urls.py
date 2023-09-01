from django.urls import path, include


from django.contrib import admin

from users.api import repot_views, user_views, certificate_views

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
    path('get-certificate-designation-content/', certificate_views.CertificateDesigAPIView.as_view()), ####
    path('get-certificate-intro/', certificate_views.CertificateIntroAPIView.as_view()), ####
    
    path('upload-cert/', certificate_views.UploadCertificateAPIView.as_view(), name='upload-certificate'),
    path('get-unique-cert-id/', certificate_views.CreateUniqueCertificateValue.as_view()),

    path('upload-file/', user_views.UserFilesAPIView.as_view(), name='upload-user-file'),

]