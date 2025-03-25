import json

from django.core.management.base import BaseCommand
from django_celery_beat.models import IntervalSchedule, PeriodicTask


class Command(BaseCommand):
    help = "Creates a Celery Beat task that runs every 10 seconds"

    def handle(self, *args, **kwargs):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=30, period=IntervalSchedule.SECONDS
        )

        _, created = PeriodicTask.objects.get_or_create(
            interval=schedule,
            name="Populate es periodically",
            task="api.tasks.populate_mock_data",
            defaults={"args": json.dumps([])},
        )

        if created:
            self.stdout.write(self.style.SUCCESS("Task scheduled successfully!"))
        else:
            self.stdout.write(self.style.WARNING("Task already exists."))
