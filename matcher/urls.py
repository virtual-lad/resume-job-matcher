from django.urls import path
from . import views

app_name = "matcher"

urlpatterns = [
    path("", views.index, name="index"),
    path("results/", views.results, name="results"),
    path("how-it-works/", views.how_it_works, name="how_it_works"),
]
