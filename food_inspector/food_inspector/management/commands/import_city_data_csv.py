from django.core.management.base import BaseCommand
from food_inspector.models import Restaurant
import csv
import food_inspector.settings.base as fsettings
from django.db import IntegrityError
from food_inspector.restaurant_finder import trim_name_for_stop_words


class Command(BaseCommand):
    help = 'Fills the database with restaurants from a city provided CSV'

    def handle(self, *args, **options):

        sfile = fsettings.BASE_DIR + '/static/csvs/Food_Inspections.csv'
        print(sfile)

        # Delete all entries from the Restaurant table
        Restaurant.objects.all().delete()

        with open(sfile) as f:
            inspection_records = [
                {k: str(v) for k, v in row.items()}
                for row in csv.DictReader(f, skipinitialspace=True)]
            self.stdout.write("Writing records to database")
            for inspection_record in inspection_records:
                try:
                    trimmed_name = trim_name_for_stop_words(
                        inspection_record["DBA Name"].upper())
                    Restaurant.objects.create(
                        chi_name=inspection_record["DBA Name"].upper(),
                        trimmed_name=trimmed_name,
                        license_number=inspection_record["License #"],
                        address=inspection_record["Address"],
                        city=inspection_record["City"],
                        zip_code=inspection_record["Zip"])
                except IntegrityError:
                    # This is a duplicate, just skip it
                    pass
        self.stdout.write("Done writing records to database")
