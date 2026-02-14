from django.urls import path
from . import views

urlpatterns = [
    path("predict/", views.predict_financials, name="predict"),
    path("chat/", views.chat_agent, name="chat"),
]
