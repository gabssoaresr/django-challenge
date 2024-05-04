from django.urls import path
from .views import GenerateMonthlyReportView

urlpatterns = [
    path('generate-report/', GenerateMonthlyReportView.generate_report, name='generate_report'),
]