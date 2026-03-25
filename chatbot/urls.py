from django.urls import path
from .views import ChatView
 
urlpatterns = [
    path('chatbot/', ChatView.as_view(), name='chatbot'),
]