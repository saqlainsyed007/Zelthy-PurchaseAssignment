from datetime import timedelta
from django.db.models import CharField, F, Func, Sum, Value
from django.db.models.functions import TruncMonth, TruncYear
from django.views.generic import TemplateView

from rest_framework.views import APIView
from rest_framework.response import Response

from purchase.choices import PurchaseStatusChoices
from purchase.models import PurchaseStatus
from purchase.serializers import PurchaseDataParamSerializer


class PurchaseDataAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    @staticmethod
    def format_data_for_chart(start_date, end_date, purchases_data):
        formatted_data = {}
        names = set(purchases_data.values_list('purchaser_name', flat=True))
        for item in purchases_data:
            purchaser_name = item['purchaser_name']
            purchase_date = item['purchase_date']
            total_quantity = item['total_quantity']
            # Create data template. All keys must be present.
            if purchase_date not in formatted_data:
                formatted_data[purchase_date] = {
                    'purchase_date': purchase_date,
                    **{name: 0 for name in names}
                }
            formatted_data[purchase_date][purchaser_name] = total_quantity
        return formatted_data.values()

    def get(self, request):
        param_serializer = PurchaseDataParamSerializer(
            data=request.GET.dict()
        )
        if not param_serializer.is_valid():
            return Response(param_serializer.errors)

        start_date = param_serializer.validated_data.get("start_date")
        end_date = param_serializer.validated_data.get("end_date")

        # Get purchase statuses that are dispatched or delivered. If a
        # purchase is dispatched and delivered, skip dispatched.
        purchase_status_ids = PurchaseStatus.objects.filter(
            status__in=[
                PurchaseStatusChoices.DISPATCHED,
                PurchaseStatusChoices.DELIVERED,
            ],
        ).order_by(
            'purchase', 'status',
        ).distinct(
            'purchase'
        ).values_list('id', flat=True)

        # No support for distinct and annotate in a single query in Django.
        purchases_data = PurchaseStatus.objects.filter(
            id__in=purchase_status_ids,
            created__gte=start_date,
            created__lte=end_date,
        ).values(
            purchaser_name=F('purchase__purchaser_name'),
            purchase_date=Func(
                F('created'),
                Value('YYYY-MM'),
                function='to_char',
                output_field=CharField()
            )
        ).annotate(
            total_quantity=Sum('purchase__quantity'),
        ).order_by(
            'purchaser_name', 'purchase_date',
        ).values(
            "purchaser_name", "purchase_date", "total_quantity",
        )

        purchases_data = self.format_data_for_chart(
            start_date, end_date, purchases_data,
        )

        return Response(purchases_data)


class PurchaseDataAnalysisView(TemplateView):
    template_name = "purchase/analyse.html"
