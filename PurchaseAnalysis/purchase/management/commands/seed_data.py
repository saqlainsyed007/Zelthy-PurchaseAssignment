import pytz
import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand

from purchase.choices import PurchaseStatusChoices
from purchase.models import Purchase, PurchaseStatus
from purchase.utils import (
    chunk_array, generate_fixed_avg_list, get_random_date,
    get_same_average_indices, rectify_same_average_by_shifting,
)


class Command(BaseCommand):

    help = 'Populate Initial Purchases Data'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.purchasers = [
            "Kati", "Amado", "Bridget", "Alton", "Julee",
            "Elvin", "Gretchen", "Alejandro", "Karlyn", "Maximo",
        ]
        self.min_quantity = 1
        self.max_quantity = 10
        self.average_quantity = 7
        self.total_purchases_required = 5000
        purchases_start_datetime_str = "2019-01-01T17:00:00+0530"
        self.purchases_start_datetime = datetime.strptime(
            purchases_start_datetime_str, '%Y-%m-%dT%H:%M:%S%z'
        ).astimezone(pytz.utc)
        purchases_end_datetime_str = "2020-03-31T22:00:00+0530"
        self.purchases_end_datetime = datetime.strptime(
            purchases_end_datetime_str, '%Y-%m-%dT%H:%M:%S%z'
        ).astimezone(pytz.utc)

    def handle(self, *args, **kwargs):
        existing_purchases = Purchase.objects.all()
        if existing_purchases:
            print("Records found. Deleting...")
            existing_purchases.delete()

        # Create 5000 purchase quantities with average of 7
        purchase_quantities = generate_fixed_avg_list(
            self.min_quantity, self.max_quantity, self.average_quantity,
            self.total_purchases_required,
        )

        # Distribute the purchases equally amongst all purchasers
        purchase_quantity_chunks = chunk_array(
            purchase_quantities, len(self.purchasers)
        )

        # Identify if there are any purchasers with same avg quantity
        same_average_indices = get_same_average_indices(
            purchase_quantity_chunks
        )

        # If there are any, move purchases(quantities) between those purchasers
        # so that their averages become different
        while same_average_indices:
            list_1_index = same_average_indices[0]
            list_2_index = same_average_indices[1]
            updated_list_1, updated_list_2 = rectify_same_average_by_shifting(
                purchase_quantity_chunks[list_1_index],
                purchase_quantity_chunks[list_2_index],
            )
            purchase_quantity_chunks[list_1_index] = updated_list_1
            purchase_quantity_chunks[list_2_index] = updated_list_2
            same_average_indices = get_same_average_indices(
                purchase_quantity_chunks
            )

        purchase_objects = []
        for purchaser_name in self.purchasers:
            purchase_quantities = purchase_quantity_chunks.pop()
            for purchase_quantity in purchase_quantities:
                purchase_objects.append(
                    Purchase(
                        purchaser_name=purchaser_name,
                        quantity=purchase_quantity,
                        created=get_random_date(
                            self.purchases_start_datetime,
                            # We leave 5 days for verification, dispatch and delivery
                            self.purchases_end_datetime - timedelta(days=5),
                        )
                    )
                )
        Purchase.objects.bulk_create(purchase_objects)

        purchase_status_objs = []
        for purchase in Purchase.objects.all():
            purchase_progress = random.randint(1, 4)
            purchase_status_objs.append(
                PurchaseStatus(
                    purchase=purchase,
                    status=PurchaseStatusChoices.OPEN,
                    created=purchase.created,
                )
            )
            if purchase_progress >= 1:
                verification_time = purchase.created + timedelta(
                    # Between 1-5 hours
                    seconds=random.randint(1*60*60, 5*60*60)
                )
                purchase_status_objs.append(
                    PurchaseStatus(
                        purchase=purchase,
                        status=PurchaseStatusChoices.VERIFIED,
                        created=verification_time,
                    )
                )
            if purchase_progress == 2:
                # Between 1-3 days post creation
                dispatch_time = purchase.created + timedelta(
                    seconds=random.randint(1*24*60*60, 3*24*60*60)
                )
                purchase_status_objs.append(
                    PurchaseStatus(
                        purchase=purchase,
                        status=PurchaseStatusChoices.DISPATCHED,
                        created=dispatch_time,
                    )
                )
            # A purchase may have a delivered status without a dispatch status
            if purchase_progress == 3:
                dispatched = random.choice([True, False])
                if dispatched:
                    # Between 1-3 days post verification
                    dispatch_time = purchase.created + timedelta(
                        seconds=random.randint(1*24*60*60, 3*24*60*60)
                    )
                    purchase_status_objs.append(
                        PurchaseStatus(
                            purchase=purchase,
                            status=PurchaseStatusChoices.DISPATCHED,
                            created=dispatch_time,
                        )
                    )
                # If an item is not dispatched, it was probably picked up
                # right away
                delivery_time = dispatch_time + timedelta(
                    # Between 0.5-2 days post dispatch
                    seconds=random.randint(0.5*24*60*60, 2*24*60*60)
                ) if dispatched else verification_time + timedelta(
                    # Between 15 - 45 min
                    seconds=random.randint(15*60, 45*60)
                )
                purchase_status_objs.append(
                    PurchaseStatus(
                        purchase=purchase,
                        status=PurchaseStatusChoices.DELIVERED,
                        created=delivery_time,
                    )
                )
        PurchaseStatus.objects.bulk_create(purchase_status_objs)
