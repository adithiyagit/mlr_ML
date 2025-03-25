import csv
from django.shortcuts import render
from .models import EnergyConsumption
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from django.shortcuts import render

def home(request):
    return render(request, 'energy/home.html')

def load_dataset():
    """Load the dataset from the CSV file into the database."""
    try:
        with open('energy_consumption.csv', newline='') as csvfile:
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
            EnergyConsumption.objects.bulk_create(data_to_insert)
            print("Dataset loaded successfully!")
    except FileNotFoundError:
        print("Error: File 'energy_consumption.csv' not found.")
    except Exception as e:
        print(f"Error loading dataset: {e}")

load_dataset()

def energy_consumption_list(request):
    data = EnergyConsumption.objects.all()
    return render(request, 'energy/list.html', {'data': data})

def train_mlr_model():
    data = EnergyConsumption.objects.all().values()
    df = pd.DataFrame(data)

    expected_columns = {'temperature', 'humidity', 'occupancy', 'hour_of_day'}
    if not expected_columns.issubset(df.columns):
        raise ValueError(f"Database columns do not match expected columns. Found: {df.columns}")

    X = df[['temperature', 'humidity', 'occupancy', 'hour_of_day']]
    y = df['energy_consumption']

    model = LinearRegression()
    model.fit(X, y)
    
    # Calculate R-squared
    y_pred = model.predict(X)
    r_squared = r2_score(y, y_pred)
    
    return model, r_squared

def predict_energy_consumption(request):
    if request.method == 'POST':
        try:
            temperature = float(request.POST.get('temperature'))
            humidity = float(request.POST.get('humidity'))
            occupancy = int(request.POST.get('occupancy'))
            hour_of_day = int(request.POST.get('hour_of_day'))

            model, r_squared = train_mlr_model()

            prediction = model.predict([[temperature, humidity, occupancy, hour_of_day]])

            return render(request, 'energy/predict.html', {
                'prediction': prediction[0],
                'temperature': temperature,
                'humidity': humidity,
                'occupancy': occupancy,
                'hour_of_day': hour_of_day,
                'r_squared': r_squared  # Pass R² score to template
            })
        except Exception as e:
            return render(request, 'energy/predict.html', {
                'error': str(e),
            })
    else:
        return render(request, 'energy/predict.html')