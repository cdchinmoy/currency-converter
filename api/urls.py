from django.urls import path, include
from .views import (CurrencyConverterApiView)

urlpatterns = [
    path('currency/convert', CurrencyConverterApiView.as_view()),
]