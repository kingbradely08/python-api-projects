#!/usr/bin/env python3
"""
Weather & Air Quality Dashboard
Get comprehensive weather information with air quality data
APIs: OpenWeatherMap, AirVisual
"""

import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import json
import argparse

# Load environment variables
load_dotenv()

class WeatherDashboard:
    def __init__(self):
        self.openweather_key = os.getenv('OPENWEATHER_API_KEY')
        self.airvisual_key = os.getenv('AIRVISUAL_API_KEY')
        self.openweather_base = 'https://api.openweathermap.org/data/2.5'
        self.airvisual_base = 'https://api.airvisual.com/v2'
        
        if not self.openweather_key:
            print("⚠️  OPENWEATHER_API_KEY not found")
            print("Get free key at: https://openweathermap.org/api")
    
    def get_current_weather(self, city, units='metric'):
        """Get current weather for a city"""
        if not self.openweather_key:
            return None
        
        endpoint = f"{self.openweather_base}/weather"
        params = {
            'q': city,
            'appid': self.openweather_key,
            'units': units
        }
        
        try:
            print(f"🌤️  Fetching current weather for {city}...")
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            weather = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'temp_min': data['main']['temp_min'],
                'temp_max': data['main']['temp_max'],
                'pressure': data['main']['pressure'],
                'humidity': data['main']['humidity'],
                'weather': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'wind_deg': data['wind'].get('deg', 0),
                'clouds': data['clouds']['all'],
                'visibility': data.get('visibility', 0),
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']),
                'timezone': data['timezone'],
                'timestamp': datetime.now()
            }
            
            return weather
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"❌ City '{city}' not found")
            else:
                print(f"❌ HTTP Error: {e}")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def get_forecast(self, city, days=5, units='metric'):
        """Get weather forecast"""
        if not self.openweather_key:
            return None
        
        endpoint = f"{self.openweather_base}/forecast"
        params = {
            'q': city,
            'appid': self.openweather_key,
            'units': units,
            'cnt': days * 8  # 8 data points per day (3-hour intervals)
        }
        
        try:
            print(f"📅 Fetching {days}-day forecast for {city}...")
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            forecast = {
                'city': data['city']['name'],
                'country': data['city']['country'],
                'forecasts': []
            }
            
            for item in data['list']:
                forecast['forecasts'].append({
                    'datetime': datetime.fromtimestamp(item['dt']),
                    'temperature': item['main']['temp'],
                    'feels_like': item['main']['feels_like'],
                    'temp_min': item['main']['temp_min'],
                    'temp_max': item['main']['temp_max'],
                    'pressure': item['main']['pressure'],
                    'humidity': item['main']['humidity'],
                    'weather': item['weather'][0]['main'],
                    'description': item['weather'][0]['description'],
                    'wind_speed': item['wind']['speed'],
                    'clouds': item['clouds']['all'],
                    'pop': item.get('pop', 0) * 100  # Probability of precipitation
                })
            
            return forecast
            
        except Exception as e:
            print(f"❌ Error fetching forecast: {e}")
            return None
    
    def get_air_quality(self, city, state=None, country=None):
        """Get air quality data"""
        if not self.airvisual_key:
            print("⚠️  AirVisual API key not configured (optional)")
            return None
        
        endpoint = f"{self.airvisual_base}/city"
        params = {
            'city': city,
            'key': self.airvisual_key
        }
        
        if state:
            params['state'] = state
        if country:
            params['country'] = country
        
        try:
            print(f"💨 Fetching air quality for {city}...")
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'success':
                current = data['data']['current']
                pollution = current['pollution']
                weather = current['weather']
                
                aqi_data = {
                    'city': data['data']['city'],
                    'state': data['data']['state'],
                    'country': data['data']['country'],
                    'aqi_us': pollution['aqius'],
                    'main_pollutant_us': pollution['mainus'],
                    'aqi_cn': pollution['aqicn'],
                    'main_pollutant_cn': pollution['maincn'],
                    'temperature': weather['tp'],
                    'humidity': weather['hu'],
                    'wind_speed': weather['ws'],
                    'timestamp': pollution['ts']
                }
                
                return aqi_data
            else:
                print(f"❌ AirVisual API Error: {data.get('message', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"❌ Error fetching air quality: {e}")
            return None
    
    def get_weather_emoji(self, weather_main):
        """Get emoji for weather condition"""
        emojis = {
            'Clear': '☀️',
            'Clouds': '☁️',
            'Rain': '🌧️',
            'Drizzle': '🌦️',
            'Thunderstorm': '⛈️',
            'Snow': '❄️',
            'Mist': '🌫️',
            'Fog': '🌫️',
            'Haze': '🌫️',
            'Smoke': '💨',
            'Dust': '💨',
            'Sand': '💨',
            'Ash': '🌋',
            'Squall': '💨',
            'Tornado': '🌪️'
        }
        return emojis.get(weather_main, '🌤️')
    
    def get_aqi_level(self, aqi):
        """Get AQI level and description"""
        if aqi <= 50:
            return 'Good', '🟢', 'Air quality is satisfactory'
        elif aqi <= 100:
            return 'Moderate', '🟡', 'Air quality is acceptable'
        elif aqi <= 150:
            return 'Unhealthy for Sensitive Groups', '🟠', 'Sensitive individuals may experience health effects'
        elif aqi <= 200:
            return 'Unhealthy', '🔴', 'Everyone may begin to experience health effects'
        elif aqi <= 300:
            return 'Very Unhealthy', '🟣', 'Health warnings of emergency conditions'
        else:
            return 'Hazardous', '🟤', 'Health alert: everyone may experience serious health effects'
    
    def display_current_weather(self, weather):
        """Display current weather information"""
        if not weather:
            return
        
        emoji = self.get_weather_emoji(weather['weather'])
        
        print(f"\n{'='*80}")
        print(f"🌤️  CURRENT WEATHER: {weather['city']}, {weather['country']}")
        print(f"{'='*80}")
        print(f"\n{emoji}  {weather['weather']} - {weather['description'].title()}")
        print(f"\n🌡️  Temperature:")
        print(f"   Current: {weather['temperature']}°C (Feels like {weather['feels_like']}°C)")
        print(f"   Min/Max: {weather['temp_min']}°C / {weather['temp_max']}°C")
        print(f"\n💧 Humidity: {weather['humidity']}%")
        print(f"🎚️  Pressure: {weather['pressure']} hPa")
        print(f"💨 Wind: {weather['wind_speed']} m/s at {weather['wind_deg']}°")
        print(f"☁️  Cloudiness: {weather['clouds']}%")
        print(f"👁️  Visibility: {weather['visibility']/1000:.1f} km")
        print(f"\n🌅 Sunrise: {weather['sunrise'].strftime('%H:%M:%S')}")
        print(f"🌇 Sunset: {weather['sunset'].strftime('%H:%M:%S')}")
        print(f"\n🕐 Updated: {weather['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
    
    def display_forecast(self, forecast):
        """Display weather forecast"""
        if not forecast:
            return
        
        print(f"\n{'='*80}")
        print(f"📅 WEATHER FORECAST: {forecast['city']}, {forecast['country']}")
        print(f"{'='*80}\n")
        
        current_date = None
        
        for item in forecast['forecasts']:
            date = item['datetime'].date()
            time = item['datetime'].strftime('%H:%M')
            
            if date != current_date:
                if current_date is not None:
                    print()
                print(f"\n📆 {date.strftime('%A, %B %d, %Y')}")
                print("-" * 80)
                current_date = date
            
            emoji = self.get_weather_emoji(item['weather'])
            pop = item['pop']
            
            print(f"  {time}: {emoji} {item['temperature']}°C - {item['description']}")
            print(f"         Feels like: {item['feels_like']}°C | Humidity: {item['humidity']}% | "
                  f"Wind: {item['wind_speed']} m/s | Rain chance: {pop:.0f}%")
    
    def display_air_quality(self, aqi_data):
        """Display air quality information"""
        if not aqi_data:
            return
        
        level, emoji, description = self.get_aqi_level(aqi_data['aqi_us'])
        
        print(f"\n{'='*80}")
        print(f"💨 AIR QUALITY: {aqi_data['city']}, {aqi_data['state']}, {aqi_data['country']}")
        print(f"{'='*80}")
        print(f"\n{emoji} AQI (US): {aqi_data['aqi_us']} - {level}")
        print(f"   {description}")
        print(f"\n🧪 Main Pollutant (US): {aqi_data['main_pollutant_us']}")
        print(f"🧪 Main Pollutant (CN): {aqi_data['main_pollutant_cn']}")
        print(f"\n🌡️  Temperature: {aqi_data['temperature']}°C")
        print(f"💧 Humidity: {aqi_data['humidity']}%")
        print(f"💨 Wind Speed: {aqi_data['wind_speed']} m/s")
        print(f"{'='*80}\n")
    
    def compare_cities(self, cities, units='metric'):
        """Compare weather across multiple cities"""
        print(f"\n{'='*80}")
        print(f"🌍 WEATHER COMPARISON")
        print(f"{'='*80}\n")
        
        results = []
        for city in cities:
            weather = self.get_current_weather(city, units)
            if weather:
                results.append(weather)
        
        if not results:
            print("❌ No weather data retrieved!")
            return
        
        # Display comparison table
        print(f"{'City':<20} {'Temp':<10} {'Weather':<20} {'Humidity':<10} {'Wind'}")
        print("-" * 80)
        
        for w in results:
            emoji = self.get_weather_emoji(w['weather'])
            print(f"{w['city']:<20} {w['temperature']:>6.1f}°C  {emoji} {w['weather']:<15} "
                  f"{w['humidity']:>3}%      {w['wind_speed']:.1f} m/s")
    
    def save_to_json(self, data, filename='weather_data.json'):
        """Save data to JSON file"""
        try:
            # Convert datetime objects to strings
            json_data = json.dumps(data, default=str, indent=2)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(json_data)
            
            print(f"✅ Data saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving to JSON: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Weather and Air Quality Dashboard',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dashboard.py --city "London"
  python dashboard.py --city "Tokyo" --forecast 7
  python dashboard.py --city "New York" --air-quality
  python dashboard.py --compare "London" "Paris" "Berlin"
  python dashboard.py --city "Mumbai" --units imperial
        """
    )
    
    parser.add_argument('--city', help='City name')
    parser.add_argument('--forecast', type=int, metavar='DAYS', help='Get forecast (1-5 days)')
    parser.add_argument('--air-quality', action='store_true', help='Get air quality data')
    parser.add_argument('--compare', nargs='+', metavar='CITY', help='Compare multiple cities')
    parser.add_argument('--units', choices=['metric', 'imperial'], default='metric',
                       help='Temperature units (default: metric)')
    parser.add_argument('--save', metavar='FILE', help='Save data to JSON file')
    
    args = parser.parse_args()
    
    dashboard = WeatherDashboard()
    
    if args.compare:
        dashboard.compare_cities(args.compare, args.units)
        return
    
    if not args.city:
        print("❌ Please specify a city with --city")
        print("Use --help for more information")
        return
    
    # Get current weather
    weather = dashboard.get_current_weather(args.city, args.units)
    dashboard.display_current_weather(weather)
    
    # Get forecast if requested
    if args.forecast:
        days = min(5, max(1, args.forecast))  # Limit to 1-5 days
        forecast = dashboard.get_forecast(args.city, days, args.units)
        dashboard.display_forecast(forecast)
    
    # Get air quality if requested
    if args.air_quality:
        aqi_data = dashboard.get_air_quality(args.city)
        dashboard.display_air_quality(aqi_data)
    
    # Save data if requested
    if args.save and weather:
        data = {
            'current': weather,
            'forecast': dashboard.get_forecast(args.city, 5, args.units) if args.forecast else None,
            'air_quality': dashboard.get_air_quality(args.city) if args.air_quality else None
        }
        dashboard.save_to_json(data, args.save)


if __name__ == "__main__":
    main()