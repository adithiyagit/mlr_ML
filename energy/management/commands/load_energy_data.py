import csv
from django.core.management.base import BaseCommand
from energy.models import EnergyConsumption

class Command(BaseCommand):
    help = 'Load data from CSV into EnergyConsumption table'

    def handle(self, *args, **kwargs):
        file_path = 'energy_consumption.csv'  # Make sure this file exists

        try:
            with open(file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                data_to_insert = [
                    EnergyConsumption(
                        temperature=float(row['Temperature']),
                        humidity=float(row['Humidity']),
                        occupancy=int(row['Occupancy']),
                        hour_of_day=int(row['Hour_of_Day']),
                        energy_consumption=float(row['Energy_Consumption'])
                    )
                    for row in reader
                ]

                # Bulk insert data
                EnergyConsumption.objects.bulk_create(data_to_insert)
                self.stdout.write(self.style.SUCCESS('✅ Data loaded successfully!'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('❌ Error: File "energy_consumption.csv" not found.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error loading data: {e}'))
