from datetime import timedelta

from django.utils import timezone

from .models import ExpiryNotification, Product


def create_expiry_notifications():
    """Create each expiry reminder once, regardless of how often this runs."""
    today = timezone.localdate()
    expiring_products = Product.objects.select_related("fridge__user").filter(
        expire_date__in=[today, today + timedelta(days=2)],
    )

    created_notifications = []
    for product in expiring_products:
        days_left = (product.expire_date - today).days
        notification_type = (
            ExpiryNotification.TODAY
            if days_left == 0
            else ExpiryNotification.TWO_DAYS
        )
        message = (
            f"Use {product.name} today — it expires today."
            if days_left == 0
            else f"{product.name} expires in 2 days. Plan a meal with it."
        )
        notification, created = ExpiryNotification.objects.get_or_create(
            user=product.fridge.user,
            product=product,
            expire_date=product.expire_date,
            notification_type=notification_type,
            defaults={
                "product_name": product.name,
                "message": message,
            },
        )
        if created:
            created_notifications.append(notification)

    return created_notifications
