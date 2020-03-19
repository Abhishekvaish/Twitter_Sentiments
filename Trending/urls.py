from django.urls import path
from . import views

app_name = 'Trending'

urlpatterns = [
    path('', views.index, name='index'),
    path('topics',views.topics, name='topics'),
    path('about',views.about,name='about'),
    path('topics/<int:id>',views.detail ,name='detail')
]
