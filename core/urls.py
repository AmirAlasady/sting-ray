
from django.urls import path
from .views import * 


urlpatterns = [

    path('',about,name='about'),
    path('showconvs',showconvs,name='showconvs'),
    path('details/<int:pk>',details,name='details'),
    path('deleate/<int:pk>',deleate,name='deleate'),
    path('ask/<int:pk>',ask,name='ask'),
    path('update/<int:pk>',update,name='update'),
    path('upload_file/<int:pk>',upload_file,name='upload_file'),
    path('deleate_file/<int:pk>/<int:id>',deleate_file,name='deleate_file')
]