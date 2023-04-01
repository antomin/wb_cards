import csv
from datetime import datetime
from os import walk

from django.conf import settings
from django.core.management.base import BaseCommand
from pymystem3 import Mystem

from tgbot_app.models import SeoWB


class Command(BaseCommand):
    @staticmethod
    def normalize_text(raw_text: str) -> str:
        mystem = Mystem()
        lemmas = mystem.lemmatize(raw_text)
        return ''.join(lemmas).strip()

    @staticmethod
    def get_file_name():
        for _, _, files in walk(f'{settings.BASE_DIR}/files'):
            return files[0]

    def save_data(self, row):
        frase, frequency = row
        lemmas = self.normalize_text(frase)
        print(frase, lemmas, frequency)

    def handle(self, *args, **options):
        file_name = self.get_file_name()
        str_date = '.'.join(file_name.split()[-1].split('.')[:3])
        _date = datetime.strptime(str_date, '%d.%m.%Y')
        print(_date)
        path = f'{settings.BASE_DIR}/files/{file_name}'
        with open(path, 'r', encoding='utf8') as file:
            reader = csv.reader(file)
            cnt = 1
            for row in reader:
                phrase, frequency, lemmas = row
                # lemmas = self.normalize_text(frase)
                new_row = SeoWB(phrase=phrase, frequency=frequency, lemmas=lemmas, created_at=_date)
                new_row.save()
                print(cnt)
                cnt += 1
