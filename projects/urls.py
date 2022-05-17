from django.urls import path

from projects.views import ProjectEnrollmentView

urlpatterns = [
    path('/enrollment', ProjectEnrollmentView.as_view()),
]
