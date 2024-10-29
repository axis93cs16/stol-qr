from django.core.management.base import BaseCommand
from datetime import datetime
from stolovaya.models import stolovaya as modelstol
from stolovaya.models import stolovayainfodata, stolovayainfopit, stolovayapodacha, stolovayacategory, get_typesofeda,get_typesofinternat, stolovayapriemipishi, stolovayamedflag, stolovayainfopitafter, stolovayafactstol
from django.core import serializers
import itertools

class Command(BaseCommand):
    help = "try to print datetime"
    def handle(self, *args, **kwargs):
#        total = kwargs['total']
#        prefix = kwargs['prefix']
        try:
            base = [modelstol.objects.all(),stolovayainfodata.objects.all(),stolovayainfopit.objects.all(),stolovayapodacha.objects.all(),stolovayacategory.objects.all(),stolovayapriemipishi.objects.all(),stolovayamedflag.objects.all(),stolovayainfopitafter.objects.all(),stolovayafactstol.objects.all()]
            flat_objects = list(itertools.chain.from_iterable(base))
            data = serializers.serialize("json", flat_objects, indent=3)
            #print(data)
            loca_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            #self.stdout.write(f"{loca_time}")
            self.stdout.write(f"{data}")
        except Exception as e:
            self.stdout.write(f"error: {e}")

