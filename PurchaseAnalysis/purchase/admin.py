from django.contrib import admin

from purchase.models import Purchase, PurchaseStatus


# Register your models here.
class PurchaseStatusInline(admin.StackedInline):
    model = PurchaseStatus
    extra = 1


class PurchaseAdmin(admin.ModelAdmin):
    model = Purchase
    inlines = [
        PurchaseStatusInline,
    ]
    list_display = (
        "id", "purchaser_name", "quantity", "created",
    )
    search_fields = (
        'purchaser_name',
    )
    list_filter = (
        "purchaser_name", "created", "updated",
    )
    readonly_fields = ("created", "updated", )

admin.site.register(Purchase, PurchaseAdmin)
