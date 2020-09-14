class PurchaseStatusChoices:
    OPEN = 1
    VERIFIED = 2
    DISPATCHED = 3
    DELIVERED = 4

    choices = (
        (OPEN, "Open"),
        (VERIFIED, "Verified"),
        (DISPATCHED, "Dispatched"),
        (DELIVERED, "Delivered"),
    )
