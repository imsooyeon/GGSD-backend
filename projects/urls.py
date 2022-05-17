from django.urls import path

from projects.views import ProjectDetailView

urlpatterns = [
    path('/<int:project_id>', ProjectDetailView.as_view()),
]
