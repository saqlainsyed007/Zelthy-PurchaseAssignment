from django.conf.urls import url

from purchase.views import PurchaseDataAPIView


urlpatterns = [
    url(r'get-purchases/', PurchaseDataAPIView.as_view(), name='purchase_data'),
]
