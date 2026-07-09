from django.contrib import admin
from django.urls import path
from ai_resumeApp import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',views.home,name="home"),
    path('result/',views.home,name="result"),
    path('scores/', views.scores, name='scores'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('resumes/', views.resume_list, name='resume_list'),
    # path('resume/<int:resume_id>/', views.resume_detail, name='resume_detail'),

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
