"""
Configuration file for News Aggregator
Contains API endpoints, categories, and default settings
"""

# API Configuration
NEWSAPI_BASE_URL = 'https://newsapi.org/v2'

# Available countries (ISO 3166-1 alpha-2 codes)
COUNTRIES = {
    'ae': 'United Arab Emirates',
    'ar': 'Argentina',
    'at': 'Austria',
    'au': 'Australia',
    'be': 'Belgium',
    'bg': 'Bulgaria',
    'br': 'Brazil',
    'ca': 'Canada',
    'ch': 'Switzerland',
    'cn': 'China',
    'co': 'Colombia',
    'cu': 'Cuba',
    'cz': 'Czech Republic',
    'de': 'Germany',
    'eg': 'Egypt',
    'fr': 'France',
    'gb': 'United Kingdom',
    'gr': 'Greece',
    'hk': 'Hong Kong',
    'hu': 'Hungary',
    'id': 'Indonesia',
    'ie': 'Ireland',
    'il': 'Israel',
    'in': 'India',
    'it': 'Italy',
    'jp': 'Japan',
    'kr': 'South Korea',
    'lt': 'Lithuania',
    'lv': 'Latvia',
    'ma': 'Morocco',
    'mx': 'Mexico',
    'my': 'Malaysia',
    'ng': 'Nigeria',
    'nl': 'Netherlands',
    'no': 'Norway',
    'nz': 'New Zealand',
    'ph': 'Philippines',
    'pl': 'Poland',
    'pt': 'Portugal',
    'ro': 'Romania',
    'rs': 'Serbia',
    'ru': 'Russia',
    'sa': 'Saudi Arabia',
    'se': 'Sweden',
    'sg': 'Singapore',
    'si': 'Slovenia',
    'sk': 'Slovakia',
    'th': 'Thailand',
    'tr': 'Turkey',
    'tw': 'Taiwan',
    'ua': 'Ukraine',
    'us': 'United States',
    've': 'Venezuela',
    'za': 'South Africa',
    'zm': 'Zambia'  # Default country 
}

# Available categories
CATEGORIES = [
    'business',
    'entertainment',
    'general',
    'health',
    'science',
    'sports',
    'technology'
]

# Available languages (ISO 639-1 codes)
LANGUAGES = {
    'ar': 'Arabic',
    'de': 'German',
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'he': 'Hebrew',
    'it': 'Italian',
    'nl': 'Dutch',
    'no': 'Norwegian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'sv': 'Swedish',
    'ud': 'Urdu',
    'zh': 'Chinese'
}

# Sort options for everything endpoint
SORT_BY_OPTIONS = {
    'relevancy': 'Articles more closely related to query come first',
    'popularity': 'Articles from popular sources and publishers come first',
    'publishedAt': 'Newest articles come first'
}

# Default settings
DEFAULT_COUNTRY = 'zm'     
DEFAULT_LANGUAGE = 'en'
DEFAULT_PAGE_SIZE = 100
DEFAULT_SORT_BY = 'publishedAt'

# API rate limits (free tier)
RATE_LIMIT_REQUESTS_PER_DAY = 100
RATE_LIMIT_REQUESTS_PER_SECOND = 5

# Request timeout (seconds)
REQUEST_TIMEOUT = 10

# Popular news sources
POPULAR_SOURCES = {
    'technology': [
        'techcrunch',
        'the-verge',
        'wired',
        'ars-technica',
        'hacker-news',
        'engadget'
    ],
    'business': [
        'bloomberg',
        'business-insider',
        'financial-times',
        'fortune',
        'the-wall-street-journal'
    ],
    'general': [
        'bbc-news',
        'cnn',
        'reuters',
        'the-washington-post',
        'the-new-york-times',
        'associated-press'
    ],
    'science': [
        'national-geographic',
        'new-scientist',
        'next-big-future'
    ],
    'entertainment': [
        'entertainment-weekly',
        'buzzfeed',
        'mtv-news'
    ],
    'sports': [
        'espn',
        'fox-sports',
        'bbc-sport',
        'nfl-news',
        'nhl-news'
    ]
}

# Output formatting
ARTICLE_DISPLAY_TEMPLATE = """
{index}. [{source}] {title}
   Author: {author}
   Published: {published_at}
   {description}
   🔗 {url}
"""

# File export settings
JSON_INDENT = 2
CSV_ENCODING = 'utf-8'

# Cache settings (optional - for future enhancement)
CACHE_ENABLED = False
CACHE_EXPIRY_MINUTES = 30
