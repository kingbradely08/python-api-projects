#!/usr/bin/env python3
"""
Multi-API Dashboard
Unified dashboard pulling data from multiple APIs simultaneously
Combines: Weather, News, Crypto, GitHub
"""

import requests
import os
from dotenv import load_dotenv
import time
import argparse
from datetime import datetime
import json

# Load environment variables
load_dotenv()

class MultiAPIDashboard:
    def __init__(self):
        # API Keys
        self.newsapi_key = os.getenv('NEWSAPI_KEY')
        self.openweather_key = os.getenv('OPENWEATHER_API_KEY')
        self.github_token = os.getenv('GITHUB_TOKEN')
        
        # API URLs
        self.news_url = 'https://newsapi.org/v2'
        self.weather_url = 'https://api.openweathermap.org/data/2.5'
        self.crypto_url = 'https://api.coingecko.com/api/v3'
        self.github_url = 'https://api.github.com'
        
        # Cache
        self.cache = {}
        self.cache_expiry = 300  # 5 minutes
        
        # Check which APIs are available
        self.check_api_status()
    
    def check_api_status(self):
        """Check which APIs are configured"""
        print("\n🔍 Checking API Configuration...\n")
        
        self.apis_available = {
            'news': bool(self.newsapi_key),
            'weather': bool(self.openweather_key),
            'crypto': True,  # CoinGecko doesn't need a key
            'github': bool(self.github_token)
        }
        
        for api, available in self.apis_available.items():
            status = "✅" if available else "❌"
            print(f"{status} {api.title()}: {'Enabled' if available else 'Disabled'}")
        print()
    
    def get_from_cache(self, key):
        """Get data from cache if not expired"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.cache_expiry:
                return data
        return None
    
    def save_to_cache(self, key, data):
        """Save data to cache"""
        self.cache[key] = (data, time.time())
    
    def fetch_news(self, category='general', country='us'):
        """Fetch latest news"""
        cache_key = f"news_{category}_{country}"
        cached = self.get_from_cache(cache_key)
        if cached:
            return cached
        
        if not self.apis_available['news']:
            return None
        
        try:
            endpoint = f"{self.news_url}/top-headlines"
            params = {
                'apiKey': self.newsapi_key,
                'category': category,
                'country': country,
                'pageSize': 5
            }
            
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get('articles', [])[:5]
            
            self.save_to_cache(cache_key, articles)
            return articles
            
        except Exception as e:
            print(f"❌ News API Error: {e}")
            return None
    
    def fetch_weather(self, city):
        """Fetch weather data"""
        cache_key = f"weather_{city}"
        cached = self.get_from_cache(cache_key)
        if cached:
            return cached
        
        if not self.apis_available['weather']:
            return None
        
        try:
            endpoint = f"{self.weather_url}/weather"
            params = {
                'q': city,
                'appid': self.openweather_key,
                'units': 'metric'
            }
            
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            weather = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'weather': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed']
            }
            
            self.save_to_cache(cache_key, weather)
            return weather
            
        except Exception as e:
            print(f"❌ Weather API Error: {e}")
            return None
    
    def fetch_crypto(self, coins=['bitcoin', 'ethereum', 'cardano']):
        """Fetch cryptocurrency prices"""
        cache_key = f"crypto_{'_'.join(coins)}"
        cached = self.get_from_cache(cache_key)
        if cached:
            return cached
        
        try:
            endpoint = f"{self.crypto_url}/simple/price"
            params = {
                'ids': ','.join(coins),
                'vs_currencies': 'usd',
                'include_24hr_change': 'true'
            }
            
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            self.save_to_cache(cache_key, data)
            return data
            
        except Exception as e:
            print(f"❌ Crypto API Error: {e}")
            return None
    
    def fetch_github_trending(self):
        """Fetch trending GitHub repositories"""
        cache_key = "github_trending"
        cached = self.get_from_cache(cache_key)
        if cached:
            return cached
        
        if not self.apis_available['github']:
            return None
        
        try:
            # Get trending repos (using search API with recent stars)
            endpoint = f"{self.github_url}/search/repositories"
            params = {
                'q': 'stars:>1000',
                'sort': 'stars',
                'order': 'desc',
                'per_page': 5
            }
            
            headers = {}
            if self.github_token:
                headers['Authorization'] = f'token {self.github_token}'
            
            response = requests.get(endpoint, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            repos = data.get('items', [])[:5]
            
            trending = []
            for repo in repos:
                trending.append({
                    'name': repo['full_name'],
                    'description': repo['description'],
                    'stars': repo['stargazers_count'],
                    'language': repo['language'],
                    'url': repo['html_url']
                })
            
            self.save_to_cache(cache_key, trending)
            return trending
            
        except Exception as e:
            print(f"❌ GitHub API Error: {e}")
            return None
    
    def display_dashboard(self, config):
        """Display the complete dashboard"""
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("="*100)
        print(f"🌐 MULTI-API DASHBOARD".center(100))
        print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(100))
        print("="*100 + "\n")
        
        # Weather Widget
        if config.get('weather'):
            weather = self.fetch_weather(config['weather_city'])
            if weather:
                self.display_weather_widget(weather)
        
        # News Widget
        if config.get('news'):
            news = self.fetch_news(config.get('news_category', 'general'))
            if news:
                self.display_news_widget(news)
        
        # Crypto Widget
        if config.get('crypto'):
            crypto = self.fetch_crypto(config.get('crypto_coins', ['bitcoin', 'ethereum']))
            if crypto:
                self.display_crypto_widget(crypto)
        
        # GitHub Widget
        if config.get('github'):
            repos = self.fetch_github_trending()
            if repos:
                self.display_github_widget(repos)
        
        print("\n" + "="*100)
        print("Press Ctrl+C to exit | Refreshes automatically")
        print("="*100)
    
    def display_weather_widget(self, weather):
        """Display weather information"""
        emoji_map = {
            'Clear': '☀️',
            'Clouds': '☁️',
            'Rain': '🌧️',
            'Snow': '❄️',
            'Thunderstorm': '⛈️'
        }
        
        emoji = emoji_map.get(weather['weather'], '🌤️')
        
        print(f"🌤️  WEATHER: {weather['city']}")
        print("-" * 100)
        print(f"{emoji} {weather['temperature']}°C (Feels like {weather['feels_like']}°C)")
        print(f"   {weather['description'].title()} | Humidity: {weather['humidity']}% | Wind: {weather['wind_speed']} m/s")
        print()
    
    def display_news_widget(self, articles):
        """Display news headlines"""
        print("📰 TOP NEWS")
        print("-" * 100)
        
        for i, article in enumerate(articles, 1):
            title = article['title'][:80] + '...' if len(article['title']) > 80 else article['title']
            source = article['source']['name']
            print(f"{i}. [{source}] {title}")
        print()
    
    def display_crypto_widget(self, crypto_data):
        """Display cryptocurrency prices"""
        print("💰 CRYPTOCURRENCY PRICES")
        print("-" * 100)
        
        for coin, data in crypto_data.items():
            price = data.get('usd', 0)
            change = data.get('usd_24h_change', 0)
            emoji = "🟢" if change >= 0 else "🔴"
            
            print(f"{coin.upper():<12} ${price:>10,.2f}  {emoji} {change:>+6.2f}%")
        print()
    
    def display_github_widget(self, repos):
        """Display GitHub trending repositories"""
        print("⭐ TRENDING GITHUB REPOSITORIES")
        print("-" * 100)
        
        for i, repo in enumerate(repos, 1):
            name = repo['name']
            stars = repo['stars']
            lang = repo.get('language', 'N/A')
            desc = repo['description'][:60] + '...' if repo['description'] and len(repo['description']) > 60 else (repo['description'] or 'No description')
            
            print(f"{i}. {name} ({lang}) - ⭐ {stars:,}")
            print(f"   {desc}")
        print()
    
    def run_dashboard(self, config, refresh_interval=60):
        """Run dashboard with auto-refresh"""
        print(f"🚀 Starting Multi-API Dashboard...")
        print(f"Refresh interval: {refresh_interval} seconds\n")
        time.sleep(2)
        
        try:
            while True:
                self.display_dashboard(config)
                time.sleep(refresh_interval)
        except KeyboardInterrupt:
            print("\n\n👋 Dashboard stopped.")
    
    def save_dashboard_config(self, config, filename='dashboard_config.json'):
        """Save dashboard configuration"""
        try:
            with open(filename, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✅ Configuration saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving config: {e}")
    
    def load_dashboard_config(self, filename='dashboard_config.json'):
        """Load dashboard configuration"""
        try:
            with open(filename, 'r') as f:
                config = json.load(f)
            print(f"✅ Configuration loaded from {filename}")
            return config
        except FileNotFoundError:
            print(f"⚠️  Config file not found, using defaults")
            return self.get_default_config()
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return self.get_default_config()
    
    def get_default_config(self):
        """Get default dashboard configuration"""
        return {
            'weather': True,
            'weather_city': 'London',
            'news': True,
            'news_category': 'technology',
            'crypto': True,
            'crypto_coins': ['bitcoin', 'ethereum', 'cardano'],
            'github': True
        }
    
    def export_dashboard_data(self, config, filename='dashboard_export.json'):
        """Export all dashboard data to JSON"""
        print("📊 Exporting dashboard data...")
        
        export_data = {
            'exported_at': datetime.now().isoformat(),
            'weather': self.fetch_weather(config['weather_city']) if config.get('weather') else None,
            'news': self.fetch_news(config.get('news_category', 'general')) if config.get('news') else None,
            'crypto': self.fetch_crypto(config.get('crypto_coins', [])) if config.get('crypto') else None,
            'github': self.fetch_github_trending() if config.get('github') else None
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, default=str)
            print(f"✅ Data exported to {filename}")
        except Exception as e:
            print(f"❌ Error exporting data: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Multi-API Dashboard - Unified data from multiple sources',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dashboard.py
  python dashboard.py --refresh 30
  python dashboard.py --city "New York" --news-category business
  python dashboard.py --config my_config.json
  python dashboard.py --export data.json
        """
    )
    
    parser.add_argument('--refresh', type=int, default=60, help='Refresh interval in seconds (default: 60)')
    parser.add_argument('--city', default='London', help='City for weather (default: London)')
    parser.add_argument('--news-category', default='technology', 
                       choices=['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology'],
                       help='News category (default: technology)')
    parser.add_argument('--crypto-coins', nargs='+', default=['bitcoin', 'ethereum', 'cardano'],
                       help='Cryptocurrency coins to track')
    parser.add_argument('--config', metavar='FILE', help='Load configuration from file')
    parser.add_argument('--save-config', metavar='FILE', help='Save current configuration')
    parser.add_argument('--export', metavar='FILE', help='Export dashboard data to JSON')
    parser.add_argument('--no-weather', action='store_true', help='Disable weather widget')
    parser.add_argument('--no-news', action='store_true', help='Disable news widget')
    parser.add_argument('--no-crypto', action='store_true', help='Disable crypto widget')
    parser.add_argument('--no-github', action='store_true', help='Disable GitHub widget')
    
    args = parser.parse_args()
    
    dashboard = MultiAPIDashboard()
    
    # Load or create configuration
    if args.config:
        config = dashboard.load_dashboard_config(args.config)
    else:
        config = {
            'weather': not args.no_weather,
            'weather_city': args.city,
            'news': not args.no_news,
            'news_category': args.news_category,
            'crypto': not args.no_crypto,
            'crypto_coins': args.crypto_coins,
            'github': not args.no_github
        }
    
    # Save configuration if requested
    if args.save_config:
        dashboard.save_dashboard_config(config, args.save_config)
        return
    
    # Export data if requested
    if args.export:
        dashboard.export_dashboard_data(config, args.export)
        return
    
    # Run dashboard
    dashboard.run_dashboard(config, args.refresh)


if __name__ == "__main__":
    main()