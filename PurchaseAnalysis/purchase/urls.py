from django.conf.urls import url

from purchase.views import PurchaseDataAnalysisView, PurchaseDataAPIView


urlpatterns = [
    url(r'get-purchases/', PurchaseDataAPIView.as_view(), name='purchase_data'),
    url(r'analyse-purchases/', PurchaseDataAnalysisView.as_view(), name='purchase_data'),
]
