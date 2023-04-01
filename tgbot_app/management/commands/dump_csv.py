import csv

from django.core.management.base import BaseCommand

from tgbot_app.models import SeoWB


class Command(BaseCommand):
    def handle(self, *args, **options):
        queryset = SeoWB.objects.all()
        with open('dump.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            cnt = 1
            for item in queryset:
                writer.writerow([item.phrase, item.frequency, item.lemmas])
                print(cnt)
                cnt += 1
