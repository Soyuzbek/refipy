from django.urls import path

from .views import application_view
from .views import confirmation_view

urlpatterns = [
    path('application/', application_view),
    path('confirmation/', confirmation_view),
]
