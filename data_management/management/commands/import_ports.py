import csv
from django.core.management.base import BaseCommand
from ports.models import Port  # Adjust this based on your actual model name


class Command(BaseCommand):
    help = "Import ports from a CSV file"

    REQUIRED_HEADERS = {'code', 'name', 'country'}  # Define required headers

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help="Path to the CSV file")

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        try:
            with open(csv_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                headers = set(reader.fieldnames) if reader.fieldnames else set()

                # Check if required headers are present
                missing_headers = self.REQUIRED_HEADERS - headers
                if missing_headers:
                    self.stderr.write(self.style.ERROR(f"Missing required headers: {', '.join(missing_headers)}"))
                    return

                count = 0
                for row in reader:
                    port, created = Port.objects.update_or_create(
                        code=row['code'].strip(),
                        defaults={
                            'port_name': row['name'].strip(),
                            'country': row['country'].strip(),
                            'city': row.get('city', '').strip(),  # Optional field
                        }
                    )
                    count += 1

                self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} ports'))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found: {csv_file}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error importing ports: {str(e)}'))
