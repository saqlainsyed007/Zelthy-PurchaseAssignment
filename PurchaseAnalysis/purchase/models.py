from django.core.validators import MinValueValidator
from django.db import models

from purchase.choices import PurchaseStatusChoices


class Purchase(models.Model):
    purchaser_name = models.CharField(
        max_length=256,
        help_text="Name of the purchaser",
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Purchase Quantity"
    )
    created = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'purchase'


class PurchaseStatus(models.Model):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        help_text="Purchase reference"
    )
    status = models.CharField(
        max_length=25,
        choices=PurchaseStatusChoices.choices,
        help_text="Status of the purchase."
    )
    created = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('purchase', 'status')
        db_table = 'purchase_status'
