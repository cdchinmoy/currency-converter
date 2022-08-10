from rest_framework.views import APIView
from .serializer import FileUploadSerializer
import pandas as pd
from django.http import HttpResponse
import requests
from django.conf import settings

def get_live_rate():
    global conversion_rate
    url = f"https://v6.exchangerate-api.com/v6/{settings.EXCHANGERATE_API_KEY}/latest/USD"
    r = requests.get(url)
    data = r.json()
    if data['result'] == 'success':
        conversion_rate = data['conversion_rates']

def get_rate(row, currency, target_currency, amount):
    currency_amount = float(conversion_rate[row[currency]])
    target_currency_amount = float(conversion_rate[row[target_currency]])
    converted_amount = (target_currency_amount / currency_amount) * row[amount]
    return str(round(converted_amount, 2))

class CurrencyConverterApiView(APIView):

    serializer_class = FileUploadSerializer

    def post(self, request):
        # try:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        converted_currency = serializer.validated_data['Converted_Currency']
        try:
            # request for live surrency rate
            get_live_rate()
            req_cols = ['Name', 'Currency', 'Amount', 'Transaction Date']
            df = pd.read_csv(file, usecols=req_cols)
            df["Converted Currency"] = converted_currency
            df["Converted Amount"] = df.apply(get_rate, axis=1, currency='Currency', target_currency="Converted Currency", amount='Amount')
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=convert.csv'
            df.to_csv(path_or_buf=response,sep=';',float_format='%.2f',index=False)
            return response
    
        except Exception as e:
            return HttpResponse(str(e))