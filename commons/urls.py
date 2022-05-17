from django.urls import path
from commons.views import FileView, MetaDataView

urlpatterns = [
    path('/file', FileView.as_view()),
    path('/meta', MetaDataView.as_view())
]