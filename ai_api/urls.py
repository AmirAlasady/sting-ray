
from django.urls import path
from .views import *



urlpatterns = [
    path('conversations', ConversationListView.as_view()),
    path('conversations/create', CreateConversationView.as_view()),
    path('conversations/<int:pk>', ConversationDetailView.as_view()),
    path('conversations/update/<int:pk>',ChangeConversationName.as_view()),
    path('files/upload/<int:pk>',FilesView.as_view()),
    path('files/show/<int:pk>',FilesView.as_view()),
    path('files/remove/<int:pk>/<int:file_id>',FilesView.as_view())
]