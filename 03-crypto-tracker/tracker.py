#!/usr/bin/env python3
"""
Cryptocurrency Tracker
Track cryptocurrency prices, portfolio value, and market trends
API: CoinGecko (no API key required)
"""

import requests
import json
import argparse
from datetime import datetime
from pathlib import Path

class CryptoTracker:
    def __init__(self):
        self.base_url = 'https://api.coingecko.com/api/v3'
        self.portfolio_file = 'crypto_portfolio.json'
        self.portfolio = self.load_portfolio()
    
    def get_coin_list(self):
        """Get list of all available cryptocurrencies"""
        endpoint = f"{self.base_url}/coins/list"
        
        try:
            response = requests.get(endpoint, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error fetching coin list: {e}")
            return []
    
    def get_price(self, coin_ids, vs_currency='usd'):
        """Get current price for cryptocurrencies"""
        endpoint = f"{self.base_url}/simple/price"
        params = {
            'ids': ','.join(coin_ids),
            'vs_currencies': vs_currency,
            'include_24hr_change': 'true',
            'include_market_cap': 'true',
            'include_24hr_vol': 'true'
        }
        
        try:
            print(f"💰 Fetching prices...")
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error fetching prices: {e}")
            return {}
    
    def get_coin_details(self, coin_id):
        """Get detailed information about a cryptocurrency"""
        endpoint = f"{self.base_url}/coins/{coin_id}"
        params = {
            'localization': 'false',
            'tickers': 'false',
            'community_data': 'false',
            'developer_data': 'false'
        }
        
        try:
            print(f"🔍 Fetching details for {coin_id}...")
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error fetching coin details: {e}")
            return None
    
    def get_market_chart(self, coin_id, vs_currency='usd', days=7):
        """Get historical market data"""
        endpoint = f"{self.base_url}/coins/{coin_id}/market_chart"
        params = {
            'vs_currency': vs_currency,
            'days': days
        }
        
        try:
            print(f"📈 Fetching {days}-day chart data...")
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error fetching chart data: {e}")
            return None
    
    def get_trending(self):
        """Get trending cryptocurrencies"""
        endpoint = f"{self.base_url}/search/trending"
        
        try:
            print("🔥 Fetching trending coins...")
            response = requests.get(endpoint, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error fetching trending: {e}")
            return None
    
    def get_top_coins(self, vs_currency='usd', limit=100, page=1):
        """Get top cryptocurrencies by market cap"""
        endpoint = f"{self.base_url}/coins/markets"
        params = {
            'vs_currency': vs_currency,
            'order': 'market_cap_desc',
            'per_page': limit,
            'page': page,
            'sparkline': 'false'
        }
        
        try:
            print(f"📊 Fetching top {limit} cryptocurrencies...")
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error fetching top coins: {e}")
            return []
    
    def load_portfolio(self):
        """Load portfolio from file"""
        if Path(self.portfolio_file).exists():
            try:
                with open(self.portfolio_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_portfolio(self):
        """Save portfolio to file"""
        try:
            with open(self.portfolio_file, 'w') as f:
                json.dump(self.portfolio, f, indent=2)
            print(f"💾 Portfolio saved to {self.portfolio_file}")
        except Exception as e:
            print(f"❌ Error saving portfolio: {e}")
    
    def add_to_portfolio(self, coin_id, amount, purchase_price=None):
        """Add coin to portfolio"""
        if coin_id not in self.portfolio:
            self.portfolio[coin_id] = []
        
        entry = {
            'amount': amount,
            'purchase_price': purchase_price,
            'date': datetime.now().isoformat()
        }
        
        self.portfolio[coin_id].append(entry)
        self.save_portfolio()
        print(f"✅ Added {amount} {coin_id.upper()} to portfolio")
    
    def calculate_portfolio_value(self, vs_currency='usd'):
        """Calculate total portfolio value"""
        if not self.portfolio:
            print("Portfolio is empty!")
            return
        
        coin_ids = list(self.portfolio.keys())
        prices = self.get_price(coin_ids, vs_currency)
        
        total_value = 0
        total_invested = 0
        
        print(f"\n{'='*100}")
        print(f"💼 PORTFOLIO VALUE")
        print(f"{'='*100}\n")
        
        print(f"{'Coin':<15} {'Amount':<15} {'Current Price':<15} {'Value':<15} {'Profit/Loss':<15}")
        print("-" * 100)
        
        for coin_id, holdings in self.portfolio.items():
            if coin_id not in prices:
                continue
            
            current_price = prices[coin_id][vs_currency]
            total_amount = sum(h['amount'] for h in holdings)
            current_value = total_amount * current_price
            
            # Calculate total invested
            invested = sum(h['amount'] * h['purchase_price'] 
                          for h in holdings if h['purchase_price'])
            
            if invested > 0:
                profit_loss = current_value - invested
                profit_loss_pct = (profit_loss / invested) * 100
                pl_str = f"${profit_loss:,.2f} ({profit_loss_pct:+.2f}%)"
                pl_emoji = "🟢" if profit_loss >= 0 else "🔴"
            else:
                pl_str = "N/A"
                pl_emoji = ""
            
            print(f"{coin_id.upper():<15} {total_amount:<15.6f} ${current_price:<14,.2f} "
                  f"${current_value:<14,.2f} {pl_emoji} {pl_str}")
            
            total_value += current_value
            if invested > 0:
                total_invested += invested
        
        print("-" * 100)
        print(f"\nTotal Portfolio Value: ${total_value:,.2f}")
        
        if total_invested > 0:
            total_pl = total_value - total_invested
            total_pl_pct = (total_pl / total_invested) * 100
            print(f"Total Invested: ${total_invested:,.2f}")
            print(f"Total Profit/Loss: ${total_pl:,.2f} ({total_pl_pct:+.2f}%)")
        
        print(f"{'='*100}\n")
    
    def display_prices(self, coin_data, vs_currency='usd'):
        """Display cryptocurrency prices"""
        print(f"\n{'='*100}")
        print(f"💰 CRYPTOCURRENCY PRICES")
        print(f"{'='*100}\n")
        
        print(f"{'Coin':<15} {'Price':<15} {'24h Change':<15} {'Market Cap':<20} {'24h Volume'}")
        print("-" * 100)
        
        for coin_id, data in coin_data.items():
            price = data.get(vs_currency, 0)
            change_24h = data.get(f'{vs_currency}_24h_change', 0)
            market_cap = data.get(f'{vs_currency}_market_cap', 0)
            volume_24h = data.get(f'{vs_currency}_24h_vol', 0)
            
            change_emoji = "🟢" if change_24h >= 0 else "🔴"
            
            print(f"{coin_id.upper():<15} ${price:<14,.2f} "
                  f"{change_emoji} {change_24h:>6.2f}%      "
                  f"${market_cap:<18,.0f} ${volume_24h:,.0f}")
        
        print(f"{'='*100}\n")
    
    def display_coin_details(self, coin_data):
        """Display detailed coin information"""
        if not coin_data:
            return
        
        print(f"\n{'='*100}")
        print(f"🪙 {coin_data['name']} ({coin_data['symbol'].upper()})")
        print(f"{'='*100}\n")
        
        # Market data
        market = coin_data.get('market_data', {})
        
        print("📊 Market Data:")
        print(f"  Current Price (USD): ${market.get('current_price', {}).get('usd', 0):,.2f}")
        print(f"  Market Cap: ${market.get('market_cap', {}).get('usd', 0):,.0f}")
        print(f"  Market Cap Rank: #{coin_data.get('market_cap_rank', 'N/A')}")
        print(f"  Total Volume: ${market.get('total_volume', {}).get('usd', 0):,.0f}")
        print(f"  24h High: ${market.get('high_24h', {}).get('usd', 0):,.2f}")
        print(f"  24h Low: ${market.get('low_24h', {}).get('usd', 0):,.2f}")
        print(f"  24h Change: {market.get('price_change_percentage_24h', 0):.2f}%")
        
        print(f"\n📈 Price Changes:")
        print(f"  7 days: {market.get('price_change_percentage_7d', 0):.2f}%")
        print(f"  30 days: {market.get('price_change_percentage_30d', 0):.2f}%")
        print(f"  1 year: {market.get('price_change_percentage_1y', 0):.2f}%")
        
        print(f"\n💎 Supply:")
        print(f"  Circulating: {market.get('circulating_supply', 0):,.0f}")
        print(f"  Total: {market.get('total_supply', 0):,.0f}")
        print(f"  Max: {market.get('max_supply', 'Unlimited')}")
        
        print(f"\n🔗 Links:")
        print(f"  Homepage: {coin_data.get('links', {}).get('homepage', ['N/A'])[0]}")
        print(f"  Blockchain: {coin_data.get('links', {}).get('blockchain_site', ['N/A'])[0]}")
        
        print(f"\n📝 Description:")
        desc = coin_data.get('description', {}).get('en', 'No description available')
        # Truncate long descriptions
        if len(desc) > 300:
            desc = desc[:297] + '...'
        print(f"  {desc}")
        
        print(f"{'='*100}\n")
    
    def display_top_coins(self, coins):
        """Display top cryptocurrencies"""
        if not coins:
            return
        
        print(f"\n{'='*120}")
        print(f"🏆 TOP CRYPTOCURRENCIES BY MARKET CAP")
        print(f"{'='*120}\n")
        
        print(f"{'#':<5} {'Coin':<20} {'Price':<15} {'24h%':<10} {'7d%':<10} {'Market Cap':<20} {'Volume (24h)'}")
        print("-" * 120)
        
        for coin in coins:
            rank = coin.get('market_cap_rank', 0)
            name = f"{coin['name']} ({coin['symbol'].upper()})"
            price = coin.get('current_price', 0)
            change_24h = coin.get('price_change_percentage_24h', 0)
            change_7d = coin.get('price_change_percentage_7d_in_currency', 0)
            market_cap = coin.get('market_cap', 0)
            volume = coin.get('total_volume', 0)
            
            change_24h_emoji = "🟢" if change_24h >= 0 else "🔴"
            change_7d_emoji = "🟢" if change_7d >= 0 else "🔴"
            
            print(f"{rank:<5} {name:<20} ${price:<14,.4f} "
                  f"{change_24h_emoji}{change_24h:>6.2f}%  "
                  f"{change_7d_emoji}{change_7d:>6.2f}%  "
                  f"${market_cap:<18,.0f} ${volume:,.0f}")
        
        print(f"{'='*120}\n")
    
    def display_trending(self, trending_data):
        """Display trending cryptocurrencies"""
        if not trending_data:
            return
        
        coins = trending_data.get('coins', [])
        
        print(f"\n{'='*80}")
        print(f"🔥 TRENDING CRYPTOCURRENCIES")
        print(f"{'='*80}\n")
        
        for i, item in enumerate(coins, 1):
            coin = item['item']
            print(f"{i}. {coin['name']} ({coin['symbol']})")
            print(f"   Market Cap Rank: #{coin.get('market_cap_rank', 'N/A')}")
            print(f"   Price (BTC): {coin.get('price_btc', 0):.8f}")
            print()
        
        print(f"{'='*80}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Cryptocurrency Tracker and Portfolio Manager',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tracker.py --price bitcoin ethereum cardano
  python tracker.py --details bitcoin
  python tracker.py --top 20
  python tracker.py --trending
  python tracker.py --portfolio
  python tracker.py --add bitcoin --amount 0.5 --purchase-price 45000
        """
    )
    
    parser.add_argument('--price', nargs='+', metavar='COIN', help='Get prices for coins')
    parser.add_argument('--details', metavar='COIN', help='Get detailed info for a coin')
    parser.add_argument('--top', type=int, metavar='N', help='Show top N coins by market cap')
    parser.add_argument('--trending', action='store_true', help='Show trending coins')
    parser.add_argument('--portfolio', action='store_true', help='Show portfolio value')
    parser.add_argument('--add', metavar='COIN', help='Add coin to portfolio')
    parser.add_argument('--amount', type=float, help='Amount to add')
    parser.add_argument('--purchase-price', type=float, help='Purchase price per coin')
    parser.add_argument('--currency', default='usd', help='Currency (default: usd)')
    
    args = parser.parse_args()
    
    tracker = CryptoTracker()
    
    if args.add:
        if not args.amount:
            print("❌ Please specify --amount")
            return
        tracker.add_to_portfolio(args.add, args.amount, args.purchase_price)
        return
    
    if args.portfolio:
        tracker.calculate_portfolio_value(args.currency)
        return
    
    if args.trending:
        trending = tracker.get_trending()
        tracker.display_trending(trending)
        return
    
    if args.top:
        coins = tracker.get_top_coins(args.currency, args.top)
        tracker.display_top_coins(coins)
        return
    
    if args.details:
        details = tracker.get_coin_details(args.details)
        tracker.display_coin_details(details)
        return
    
    if args.price:
        prices = tracker.get_price(args.price, args.currency)
        tracker.display_prices(prices, args.currency)
        return
    
    print("❌ Please specify an action")
    print("Use --help for more information")


if __name__ == "__main__":
    main()