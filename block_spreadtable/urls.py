from django.urls import path
from . import views

urlpatterns = [
    path(
        'block_spreadtable/',
        views.BlockSpreadTaleView.as_view(),
        name='block_spreadtable'
    ),
]
