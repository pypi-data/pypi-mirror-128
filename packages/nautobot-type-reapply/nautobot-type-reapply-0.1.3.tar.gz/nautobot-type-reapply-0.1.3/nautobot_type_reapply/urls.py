from __future__ import unicode_literals

from django.urls import path

from . import views

app_name = 'nautobot_type_reapply'
urlpatterns = [
    path(r'reapply/<uuid:pk>/edit/', views.ReapplyView.as_view(), name='reapply'),
]
