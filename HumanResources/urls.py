from django.urls import path
from .views.vacant_position_view import CustomFieldVacantPositionListCreateView, VacantPositionListCreateView, CustomFieldVacantPositionDeleteView, VacantPositionDeleteView, VacantPositionApproveView
from .views.candidate_view import CustomFieldCandidateListCreateView, CandidateListCreateView, CustomFieldCandidateDeleteView, CandidateDeleteView, CandidateApproveView
from .views.vacant_position_agent_view import publish_vacant_description

urlpatterns = [
    # Vacantes
    path("vacant_position/custom_fields/", CustomFieldVacantPositionListCreateView.as_view(), name="campos"),
    path("vacant_position/custom_fields/<int:pk>/delete/", CustomFieldVacantPositionDeleteView.as_view(), name="campo_delete"),
    path("vacant_position/", VacantPositionListCreateView.as_view(), name="vacantes"),
    path("vacant_position/<int:pk>/delete/", VacantPositionDeleteView.as_view(), name="vacante_delete"),
    path("vacant_position/<int:pk>/approve/", VacantPositionApproveView.as_view(), name="vacante_approve"),
    # Candidatos
    path("candidate/custom_fields/", CustomFieldCandidateListCreateView.as_view(), name="campos"),
    path("candidate/custom_fields/<int:pk>/delete/", CustomFieldCandidateDeleteView.as_view(), name="campo_delete"),
    path("candidate/", CandidateListCreateView.as_view(), name="vacantes"),
    path("candidate/<int:pk>/delete/", CandidateDeleteView.as_view(), name="vacante_delete"),
    path("candidate/<int:pk>/approve/", CandidateApproveView.as_view(), name="vacante_approve"),    
    # Agente de IA
    path("vacant_position/description_generator/<int:pk>/", publish_vacant_description.as_view(), name="vacante_descripcion_ia"),
]
