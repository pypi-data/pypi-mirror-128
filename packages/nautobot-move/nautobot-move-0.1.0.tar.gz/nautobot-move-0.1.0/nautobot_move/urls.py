from __future__ import unicode_literals

from django.urls import path

from . import views

app_name = "nautobot_move"
urlpatterns = [
    path(r"move/<uuid:pk>/edit/", views.MoveView.as_view(), name="move"),
]
