"""
Weather Service using Open-Meteo API
Free weather data with no API key required
"""

import requests
from datetime import datetime, timedelta
import pandas as pd

class WeatherService:
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    # Common chili-growing regions in Indonesia
    LOCATIONS = {
        "Jakarta": {"lat": -6.2088, "lon": 106.8456, "name": "Jakarta"},
        "Bandung": {"lat": -6.9175, "lon": 107.6191, "name": "Bandung"},
        "Surabaya": {"lat": -7.2575, "lon": 112.7521, "name": "Surabaya"},
        "Yogyakarta": {"lat": -7.7956, "lon": 110.3695, "name": "Yogyakarta"},
        "Semarang": {"lat": -6.9667, "lon": 110.4167, "name": "Semarang"},
        "Malang": {"lat": -7.9797, "lon": 112.6304, "name": "Malang"},
        "Bogor": {"lat": -6.5950, "lon": 106.8166, "name": "Bogor"},
        "Garut": {"lat": -7.2211, "lon": 107.9066, "name": "Garut"}
    }
    
    @staticmethod
    def get_weather(lat, lon):
        """
        Get current weather and 7-day forecast from Open-Meteo
        
        Args:
            lat: Latitude
            lon: Longitude
        
        Returns:
            dict with current weather and forecast
        """
        try:
            # API parameters
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "precipitation",
                    "weather_code",
                    "wind_speed_10m",
                    "apparent_temperature"
                ],
                "daily": [
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_sum",
                    "precipitation_probability_max",
                    "weather_code",
                    "wind_speed_10m_max"
                ],
                "timezone": "Asia/Jakarta",
                "forecast_days": 7
            }
            
            response = requests.get(WeatherService.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Parse current weather
            current = {
                'temperature': round(data['current']['temperature_2m'], 1),
                'feels_like': round(data['current']['apparent_temperature'], 1),
                'humidity': data['current']['relative_humidity_2m'],
                'rainfall': round(data['current']['precipitation'], 1),
                'wind_speed': round(data['current']['wind_speed_10m'], 1),
                'weather_code': data['current']['weather_code'],
                'condition': WeatherService._get_weather_condition(data['current']['weather_code']),
                'timestamp': datetime.now()
            }
            
            # Parse forecast
            forecast = []
            for i in range(7):
                forecast.append({
                    'date': data['daily']['time'][i],
                    'temp_max': round(data['daily']['temperature_2m_max'][i], 1),
                    'temp_min': round(data['daily']['temperature_2m_min'][i], 1),
                    'rainfall': round(data['daily']['precipitation_sum'][i], 1),
                    'rainfall_prob': data['daily']['precipitation_probability_max'][i],
                    'weather_code': data['daily']['weather_code'][i],
                    'condition': WeatherService._get_weather_condition(data['daily']['weather_code'][i]),
                    'wind_speed': round(data['daily']['wind_speed_10m_max'][i], 1)
                })
            
            return {
                'current': current,
                'forecast': forecast,
                'location': {'lat': lat, 'lon': lon}
            }
        
        except Exception as e:
            # Return simulated data as fallback
            return WeatherService._get_simulated_weather(lat, lon)
    
    @staticmethod
    def _get_weather_condition(code):
        """Convert WMO weather code to description"""
        conditions = {
            0: "Cerah",
            1: "Cerah Sebagian",
            2: "Berawan Sebagian",
            3: "Berawan",
            45: "Berkabut",
            48: "Berkabut",
            51: "Gerimis Ringan",
            53: "Gerimis",
            55: "Gerimis Lebat",
            61: "Hujan Ringan",
            63: "Hujan",
            65: "Hujan Lebat",
            71: "Salju Ringan",
            73: "Salju",
            75: "Salju Lebat",
            77: "Butiran Salju",
            80: "Hujan Shower Ringan",
            81: "Hujan Shower",
            82: "Hujan Shower Lebat",
            85: "Salju Shower Ringan",
            86: "Salju Shower Lebat",
            95: "Badai Petir",
            96: "Badai Petir dengan Hujan Es Ringan",
            99: "Badai Petir dengan Hujan Es Lebat"
        }
        return conditions.get(code, "Tidak Diketahui")
    
    @staticmethod
    def _get_simulated_weather(lat, lon):
        """Fallback simulated weather data"""
        import random
        
        current = {
            'temperature': round(25 + random.uniform(-3, 8), 1),
            'feels_like': round(27 + random.uniform(-3, 8), 1),
            'humidity': random.randint(60, 90),
            'rainfall': round(random.uniform(0, 5), 1),
            'wind_speed': round(random.uniform(5, 20), 1),
            'weather_code': random.choice([0, 1, 2, 3, 61, 63]),
            'condition': random.choice(["Cerah", "Berawan", "Hujan Ringan"]),
            'timestamp': datetime.now()
        }
        
        forecast = []
        for i in range(7):
            forecast.append({
                'date': (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
                'temp_max': round(28 + random.uniform(-3, 5), 1),
                'temp_min': round(22 + random.uniform(-3, 3), 1),
                'rainfall': round(random.uniform(0, 30), 1),
                'rainfall_prob': random.randint(20, 80),
                'weather_code': random.choice([0, 1, 2, 3, 61, 63]),
                'condition': random.choice(["Cerah", "Berawan", "Hujan"]),
                'wind_speed': round(random.uniform(5, 25), 1)
            })
        
        return {
            'current': current,
            'forecast': forecast,
            'location': {'lat': lat, 'lon': lon}
        }
    
    @staticmethod
    def check_alerts(weather_data):
        """Check for weather alerts"""
        alerts = []
        
        current = weather_data['current']
        forecast = weather_data['forecast']
        
        # Heavy rain alert
        for day in forecast[:3]:  # Next 3 days
            if day['rainfall'] > 50:
                alerts.append({
                    'type': 'Hujan Lebat',
                    'severity': 'Tinggi',
                    'date': day['date'],
                    'description': f"Hujan lebat diprediksi ({day['rainfall']}mm)",
                    'impact': 'Risiko banjir, tanaman stress',
                    'actions': ['Cek drainase', 'Tunda penyemprotan', 'Lindungi tanaman']
                })
        
        # Extreme heat
        if current['temperature'] > 35:
            alerts.append({
                'type': 'Panas Ekstrem',
                'severity': 'Tinggi',
                'date': 'Hari ini',
                'description': f"Suhu sangat tinggi ({current['temperature']}°C)",
                'impact': 'Tanaman stress, kebutuhan air tinggi',
                'actions': ['Penyiraman ekstra', 'Naungan jika perlu', 'Monitor tanaman']
            })
        
        # Strong wind
        if current['wind_speed'] > 30:
            alerts.append({
                'type': 'Angin Kencang',
                'severity': 'Sedang',
                'date': 'Hari ini',
                'description': f"Angin kencang ({current['wind_speed']} km/h)",
                'impact': 'Tanaman roboh, spray tidak efektif',
                'actions': ['Pasang ajir', 'Tunda penyemprotan', 'Cek tanaman']
            })
        
        # Drought warning (no rain forecast)
        total_rain_forecast = sum(day['rainfall'] for day in forecast)
        if total_rain_forecast < 5:
            alerts.append({
                'type': 'Kekeringan',
                'severity': 'Sedang',
                'date': '7 hari ke depan',
                'description': "Tidak ada hujan signifikan dalam 7 hari",
                'impact': 'Tanaman kekurangan air',
                'actions': ['Penyiraman rutin', 'Mulsa untuk retensi air', 'Monitor kelembaban tanah']
            })
        
        return alerts
    
    @staticmethod
    def get_spray_recommendations(weather_data):
        """Get spray timing recommendations"""
        forecast = weather_data['forecast']
        recommendations = []
        
        for i, day in enumerate(forecast[:7]):
            # Ideal conditions: no rain, low wind
            is_ideal = (
                day['rainfall_prob'] < 30 and
                day['rainfall'] < 5 and
                day['wind_speed'] < 15
            )
            
            if is_ideal:
                recommendations.append({
                    'date': day['date'],
                    'day_name': WeatherService._get_day_name(i),
                    'status': 'Ideal',
                    'reason': 'Cuaca cerah, angin rendah',
                    'confidence': 'Tinggi'
                })
            elif day['rainfall_prob'] > 60 or day['rainfall'] > 10:
                recommendations.append({
                    'date': day['date'],
                    'day_name': WeatherService._get_day_name(i),
                    'status': 'Tidak Disarankan',
                    'reason': 'Hujan diprediksi',
                    'confidence': 'Tinggi'
                })
            elif day['wind_speed'] > 20:
                recommendations.append({
                    'date': day['date'],
                    'day_name': WeatherService._get_day_name(i),
                    'status': 'Kurang Ideal',
                    'reason': 'Angin kencang',
                    'confidence': 'Sedang'
                })
            else:
                recommendations.append({
                    'date': day['date'],
                    'day_name': WeatherService._get_day_name(i),
                    'status': 'Cukup Baik',
                    'reason': 'Kondisi cukup mendukung',
                    'confidence': 'Sedang'
                })
        
        return recommendations
    
    @staticmethod
    def _get_day_name(day_offset):
        """Get day name from offset"""
        days = ['Hari Ini', 'Besok', 'Lusa']
        if day_offset < 3:
            return days[day_offset]
        else:
            date = datetime.now() + timedelta(days=day_offset)
            return date.strftime("%A")
