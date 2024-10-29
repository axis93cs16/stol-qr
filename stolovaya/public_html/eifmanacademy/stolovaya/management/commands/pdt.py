from django.core.management.base import BaseCommand
from datetime import datetime

class Command(BaseCommand):
    help = "try to print datetime"
    def handle(self, *args, **kwargs):
#        total = kwargs['total']
#        prefix = kwargs['prefix']
        try:
            loca_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            self.stdout.write(f"datetime = {loca_time}")
        except Exception as e:
            self.stdout.write(f"error: {e}")

