from django.urls import path
from .views import AdminPanelView, AnalysisView


urlpatterns = [
    path('', AdminPanelView.as_view(), name='admin-panel'),
    path('analysis/', AnalysisView.as_view(), name='analysis'),
]