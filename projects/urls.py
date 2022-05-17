from django.urls import path

from projects.views import ProjectsListView

urlpatterns = [
    path('', ProjectsListView.as_view()),
]
