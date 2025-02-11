import csv
from django.core.management.base import BaseCommand
from ports.models import Port  # Adjust this based on your actual model name

class Command(BaseCommand):
    help = "Import ports from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help="Path to the CSV file")

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        try:
            with open(csv_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                count = 0

                for row in reader:
                    port, created = Port.objects.update_or_create(
                        code=row['code'],  # Adjust column names based on your CSV
                        defaults={
                            'port_name': row['name'],
                            'country': row['country'],
                            'city': row.get('city', ''),  # Optional fields
                        }
                    )
                    count += 1

                self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} ports'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error importing ports: {str(e)}'))
