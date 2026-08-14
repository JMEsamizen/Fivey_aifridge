from django.core.management.base import BaseCommand

from fridge.services import create_expiry_notifications


class Command(BaseCommand):
    help = "Create reminders for products expiring today or in two days."

    def handle(self, *args, **options):
        notifications = create_expiry_notifications()
        self.stdout.write(
            self.style.SUCCESS(f"Created {len(notifications)} expiry notification(s).")
        )
