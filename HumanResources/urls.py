from django.urls import path
from .views.vacant_position_view import CustomFieldListCreateView, VacantPositionListCreateView, CustomFieldDeleteView

urlpatterns = [
    path("custom_fields/", CustomFieldListCreateView.as_view(), name="campos"),
    path("custom_fields/<int:pk>/delete/", CustomFieldDeleteView.as_view(), name="campo_delete"),
    path("vacant_position/", VacantPositionListCreateView.as_view(), name="vacantes"),
]
