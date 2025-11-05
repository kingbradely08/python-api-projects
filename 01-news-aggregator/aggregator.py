#!/usr/bin/env python3
"""
Multi-Source News Aggregator
Aggregate news from multiple sources with filtering and search
API: NewsAPI (https://newsapi.org/)
"""

import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import json
import argparse

# Load environment variables
load_dotenv()

class NewsAggregator:
    def __init__(self):
        self.newsapi_key = os.getenv('NEWSAPI_KEY')
        self.base_url = 'https://newsapi.org/v2'
        self.articles = []
        
        if not self.newsapi_key:
            print("⚠️  Warning: NEWSAPI_KEY not found in environment variables")
            print("Get a free key at: https://newsapi.org/register")
    
    def get_top_headlines(self, country='us', category=None, query=None):
        """Get top headlines"""
        if not self.newsapi_key:
            print("❌ API key required!")
            return []
        
        endpoint = f"{self.base_url}/top-headlines"
        params = {
            'apiKey': self.newsapi_key,
            'country': country,
            'pageSize': 100
        }
        
        if category:
            params['category'] = category
        if query:
            params['q'] = query
        
        print(f"🔍 Fetching top headlines...")
        if category:
            print(f"   Category: {category}")
        if query:
            print(f"   Query: {query}")
        print()
        
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'ok':
                articles = data.get('articles', [])
                self.articles.extend(self._process_articles(articles, 'NewsAPI'))
                print(f"✅ Found {len(articles)} articles")
                return articles
            else:
                print(f"❌ API Error: {data.get('message', 'Unknown error')}")
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return []
    
    def search_everything(self, query, from_date=None, to_date=None, language='en', sort_by='publishedAt'):
        """Search all articles"""
        if not self.newsapi_key:
            print("❌ API key required!")
            return []
        
        endpoint = f"{self.base_url}/everything"
        params = {
            'apiKey': self.newsapi_key,
            'q': query,
            'language': language,
            'sortBy': sort_by,
            'pageSize': 100
        }
        
        if from_date:
            params['from'] = from_date
        if to_date:
            params['to'] = to_date
        
        print(f"🔍 Searching for: '{query}'")
        print(f"   Language: {language}")
        print(f"   Sort by: {sort_by}\n")
        
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'ok':
                articles = data.get('articles', [])
                self.articles.extend(self._process_articles(articles, 'NewsAPI'))
                print(f"✅ Found {len(articles)} articles")
                return articles
            else:
                print(f"❌ API Error: {data.get('message', 'Unknown error')}")
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return []
    
    def get_sources(self, category=None, language='en', country=None):
        """Get available news sources"""
        if not self.newsapi_key:
            print("❌ API key required!")
            return []
        
        endpoint = f"{self.base_url}/top-headlines/sources"
        params = {
            'apiKey': self.newsapi_key,
            'language': language
        }
        
        if category:
            params['category'] = category
        if country:
            params['country'] = country
        
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'ok':
                return data.get('sources', [])
            else:
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching sources: {e}")
            return []
    
    def _process_articles(self, articles, source_name):
        """Process and normalize articles"""
        processed = []
        
        for article in articles:
            processed.append({
                'source': article.get('source', {}).get('name', source_name),
                'author': article.get('author', 'Unknown'),
                'title': article.get('title', 'No title'),
                'description': article.get('description', 'No description'),
                'url': article.get('url', ''),
                'published_at': article.get('publishedAt', ''),
                'content': article.get('content', '')
            })
        
        return processed
    
    def remove_duplicates(self):
        """Remove duplicate articles by title"""
        seen_titles = set()
        unique_articles = []
        
        for article in self.articles:
            title = article['title'].lower()
            if title not in seen_titles:
                seen_titles.add(title)
                unique_articles.append(article)
        
        duplicates_removed = len(self.articles) - len(unique_articles)
        self.articles = unique_articles
        
        if duplicates_removed > 0:
            print(f"🧹 Removed {duplicates_removed} duplicate(s)")
    
    def filter_by_keyword(self, keyword):
        """Filter articles by keyword in title or description"""
        keyword_lower = keyword.lower()
        filtered = [
            article for article in self.articles
            if keyword_lower in article['title'].lower() 
            or keyword_lower in article['description'].lower()
        ]
        
        print(f"🔍 Filtered to {len(filtered)} articles containing '{keyword}'")
        return filtered
    
    def sort_articles(self, by='date', reverse=True):
        """Sort articles"""
        if by == 'date':
            self.articles.sort(
                key=lambda x: x['published_at'] or '', 
                reverse=reverse
            )
        elif by == 'source':
            self.articles.sort(
                key=lambda x: x['source'], 
                reverse=reverse
            )
        
        print(f"✅ Sorted by {by}")
    
    def display_articles(self, limit=10):
        """Display articles in formatted output"""
        if not self.articles:
            print("\n❌ No articles to display!")
            return
        
        articles_to_show = self.articles[:limit]
        
        print(f"\n{'='*100}")
        print(f"📰 NEWS ARTICLES ({len(self.articles)} total, showing {len(articles_to_show)})")
        print(f"{'='*100}\n")
        
        for i, article in enumerate(articles_to_show, 1):
            # Format published date
            pub_date = article['published_at']
            if pub_date:
                try:
                    dt = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                    pub_date = dt.strftime('%Y-%m-%d %H:%M')
                except:
                    pass
            
            print(f"{i}. [{article['source']}] {article['title']}")
            print(f"   Author: {article['author']}")
            print(f"   Published: {pub_date}")
            print(f"   {article['description'][:150]}...")
            print(f"   🔗 {article['url']}")
            print()
    
    def save_to_json(self, filename='news_articles.json'):
        """Save articles to JSON file"""
        if not self.articles:
            print("❌ No articles to save!")
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.articles, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Saved {len(self.articles)} articles to {filename}")
        except Exception as e:
            print(f"❌ Error saving to JSON: {e}")
    
    def save_to_csv(self, filename='news_articles.csv'):
        """Save articles to CSV file"""
        if not self.articles:
            print("❌ No articles to save!")
            return
        
        try:
            import csv
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['source', 'author', 'title', 'description', 'url', 'published_at']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                writer.writeheader()
                for article in self.articles:
                    writer.writerow({k: article.get(k, '') for k in fieldnames})
            
            print(f"✅ Saved {len(self.articles)} articles to {filename}")
        except Exception as e:
            print(f"❌ Error saving to CSV: {e}")
    
    def display_sources(self, sources):
        """Display available sources"""
        if not sources:
            print("No sources found!")
            return
        
        print(f"\n📡 AVAILABLE NEWS SOURCES ({len(sources)})")
        print("="*80)
        
        for source in sources:
            print(f"\n{source['name']}")
            print(f"  ID: {source['id']}")
            print(f"  Category: {source.get('category', 'N/A')}")
            print(f"  Language: {source.get('language', 'N/A')}")
            print(f"  Country: {source.get('country', 'N/A')}")
            print(f"  Description: {source.get('description', 'N/A')}")
            print(f"  URL: {source.get('url', 'N/A')}")


def main():
    parser = argparse.ArgumentParser(
        description='Aggregate news from multiple sources',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python aggregator.py --headlines --country us
  python aggregator.py --headlines --category technology
  python aggregator.py --search "artificial intelligence" --limit 20
  python aggregator.py --search "climate change" --from 2024-01-01
  python aggregator.py --sources --category business
        """
    )
    
    parser.add_argument('--headlines', action='store_true', help='Get top headlines')
    parser.add_argument('--search', metavar='QUERY', help='Search for specific topic')
    parser.add_argument('--sources', action='store_true', help='List available sources')
    
    parser.add_argument('--country', default='us', help='Country code (default: us)')
    parser.add_argument('--category', choices=['business', 'entertainment', 'general', 
                                               'health', 'science', 'sports', 'technology'],
                       help='News category')
    parser.add_argument('--language', default='en', help='Language code (default: en)')
    
    parser.add_argument('--from', dest='from_date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--to', dest='to_date', help='End date (YYYY-MM-DD)')
    parser.add_argument('--sort', choices=['relevancy', 'popularity', 'publishedAt'],
                       default='publishedAt', help='Sort order')
    
    parser.add_argument('--limit', type=int, default=10, help='Number of articles to display')
    parser.add_argument('--save-json', metavar='FILE', help='Save to JSON file')
    parser.add_argument('--save-csv', metavar='FILE', help='Save to CSV file')
    
    args = parser.parse_args()
    
    aggregator = NewsAggregator()
    
    # Fetch data based on command
    if args.sources:
        sources = aggregator.get_sources(args.category, args.language, args.country)
        aggregator.display_sources(sources)
        return
    
    if args.headlines:
        aggregator.get_top_headlines(args.country, args.category, args.search)
    elif args.search:
        aggregator.search_everything(
            args.search, 
            args.from_date, 
            args.to_date, 
            args.language, 
            args.sort
        )
    else:
        print("❌ Please specify --headlines or --search")
        print("Use --help for more information")
        return
    
    # Process articles
    aggregator.remove_duplicates()
    aggregator.sort_articles('date')
    
    # Display results
    aggregator.display_articles(args.limit)
    
    # Save if requested
    if args.save_json:
        aggregator.save_to_json(args.save_json)
    
    if args.save_csv:
        aggregator.save_to_csv(args.save_csv)


if __name__ == "__main__":
    main()