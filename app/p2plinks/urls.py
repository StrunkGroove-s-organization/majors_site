from django.urls import path
from . import views

app_name = 'p2plinks'

urlpatterns = [
    path('spreadtable/', views.SpreadTableView.as_view(), name='spreadtable'),
    path('api/p2plinks_2/', views.P2PLinks2View.as_view(), name='p2plinks_2'),
    path('api/p2plinks_3/', views.P2PLinks3View.as_view(), name='p2plinks_3'),
]
