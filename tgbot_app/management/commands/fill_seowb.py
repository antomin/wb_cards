from django.conf import settings
from django.core.management.base import BaseCommand
from openpyxl import load_workbook

from tgbot_app.models import SeoWB


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Open file...')
        wb = load_workbook(f'{settings.BASE_DIRpyt}/seowb.xlsx')

        sheet = wb['WB']

        for i in range(1, 1000001):
            frase = sheet[f'A{i}'].value
            val = sheet[f'B{i}'].value

            print(i)

            new_str = SeoWB(frase=frase, frequency=int(val))
            new_str.save()

        print('Done!')
