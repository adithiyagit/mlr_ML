from django.db import models

class EnergyConsumption(models.Model):
    temperature = models.FloatField()  # Temperature in °C
    humidity = models.FloatField()     # Humidity in %
    occupancy = models.IntegerField()  # Number of people
    hour_of_day = models.IntegerField()  # Hour of the day (0-23)
    energy_consumption = models.FloatField()  # Energy consumption in kWh

    def __str__(self):
        return f"Energy Consumption at {self.hour_of_day}:00"