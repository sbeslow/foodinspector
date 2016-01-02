from django.core.management.base import BaseCommand
from food_inspector.models import Restaurant
import csv
import food_inspector.settings.base as fsettings
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Fills the database with restaurants from a city provided CSV'

    def handle(self, *args, **options):

        sfile = fsettings.BASE_DIR + '/static/Food_Inspections.csv'
        print(sfile)

        with open(sfile) as f:
            inspection_records = [
                {k: str(v) for k, v in row.items()}
                for row in csv.DictReader(f, skipinitialspace=True)]
            self.stdout.write("Writing records to database")
            for inspection_record in inspection_records:
                try:
                    Restaurant.objects.create(
                        name=inspection_record["DBA Name"],
                        license_number=inspection_record["License #"],
                        address=inspection_record["Address"],
                        city=inspection_record["City"],
                        zip_code=inspection_record["Zip"])
                except IntegrityError:
                    # This is a duplicate, just skip it
                    pass
        self.stdout.write("Done writing records to database")
