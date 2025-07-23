from django.urls import path

from Training.views.lesson_view import CustomFieldLessonDeleteView, CustomFieldLessonListCreateView, LessonApproveView, LessonDeleteView, LessonListCreateView

urlpatterns = [
    # Clases
    path("lesson/custom_fields/", CustomFieldLessonListCreateView.as_view(), name="campos"),
    path("lesson/custom_fields/<int:pk>/delete/", CustomFieldLessonDeleteView.as_view(), name="campo_delete"),
    path("lesson/", LessonListCreateView.as_view(), name="clases"),
    path("lesson/<int:pk>/delete/", LessonDeleteView.as_view(), name="clase_delete"),
    path("lesson/<int:pk>/approve/", LessonApproveView.as_view(), name="clase_approve"),
]