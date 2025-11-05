# Python API Integration Projects

A comprehensive collection of real-world API integration projects demonstrating REST API consumption, authentication methods, data handling, and practical applications.

## 🎯 Repository Focus

This repository showcases:
- RESTful API consumption
- API authentication (API keys, OAuth, tokens)
- JSON data parsing and manipulation
- Error handling and rate limiting
- Real-time data fetching
- Multi-API orchestration
- Environment variable management

## 📚 Projects

### 1. Multi-Source News Aggregator
**Difficulty:** Beginner  
**APIs Used:** NewsAPI, Guardian API, New York Times API

Aggregate news from multiple sources with filtering and search capabilities.

**Features:**
- Fetch news from 3+ sources
- Filter by category, country, language
- Search by keywords
- Sort by relevance/date
- Save articles to JSON/CSV
- Remove duplicate articles
- Display in formatted CLI

**API Keys Required:** NewsAPI (free tier available)

---

### 2. Weather & Air Quality Dashboard
**Difficulty:** Beginner-Intermediate  
**APIs Used:** OpenWeatherMap, AirVisual, WeatherAPI

Comprehensive weather information with air quality data and forecasts.

**Features:**
- Current weather conditions
- 7-day forecast
- Air quality index (AQI)
- UV index and alerts
- Multiple location support
- Weather comparison
- Historical data tracking
- JSON/CSV export

**API Keys Required:** OpenWeatherMap, AirVisual (free tiers available)

---

### 3. Cryptocurrency Tracker
**Difficulty:** Intermediate  
**APIs Used:** CoinGecko, CoinCap, Binance

Track cryptocurrency prices, portfolio value, and market trends.

**Features:**
- Real-time price tracking
- Portfolio management
- Price alerts (above/below threshold)
- Historical price charts
- Market cap rankings
- Convert between currencies
- Profit/loss calculator
- Export portfolio data

**API Keys Required:** CoinGecko (no key needed), Binance (optional)

---

### 4. GitHub Repository Analytics
**Difficulty:** Intermediate  
**APIs Used:** GitHub REST API, GitHub GraphQL API

Analyze GitHub repositories with detailed statistics and visualizations.

**Features:**
- Repository statistics
- Contributor analysis
- Commit history trends
- Language breakdown
- Star/fork history
- Issue tracking
- Pull request analytics
- Compare multiple repos
- Generate reports

**API Keys Required:** GitHub Personal Access Token (free)

---

### 5. Email & SMS Notification System
**Difficulty:** Intermediate-Advanced  
**APIs Used:** SendGrid, Twilio, Mailgun

Automated notification system supporting email and SMS.

**Features:**
- Send emails with templates
- Send SMS notifications
- Bulk messaging
- Scheduled notifications
- Email validation
- Delivery status tracking
- Template management
- Contact list management
- Retry logic

**API Keys Required:** SendGrid/Mailgun (free tier), Twilio (trial credits)

---

### 6. Multi-API Dashboard
**Difficulty:** Advanced  
**APIs Used:** Multiple (weather, news, stocks, crypto, GitHub)

Unified dashboard pulling data from multiple APIs simultaneously.

**Features:**
- Real-time data from 5+ APIs
- Customizable widgets
- Auto-refresh intervals
- Data caching
- Rate limit handling
- Error recovery
- Export all data
- Configuration management
- Responsive CLI dashboard

**API Keys Required:** Various (based on enabled features)

---

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.8 or higher
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/b5119/python-api-projects.git
cd python-api-projects
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your API keys
nano .env  # or use your preferred editor
```

### Environment Variables

Create a `.env` file in the root directory:

```env
# News APIs
NEWSAPI_KEY=your_newsapi_key_here
GUARDIAN_API_KEY=your_guardian_key_here
NYT_API_KEY=your_nyt_key_here

# Weather APIs
OPENWEATHER_API_KEY=your_openweather_key_here
AIRVISUAL_API_KEY=your_airvisual_key_here

# Crypto APIs (optional)
BINANCE_API_KEY=your_binance_key_here
BINANCE_SECRET_KEY=your_binance_secret_here

# GitHub
GITHUB_TOKEN=your_github_token_here

# Notifications
SENDGRID_API_KEY=your_sendgrid_key_here
TWILIO_ACCOUNT_SID=your_twilio_sid_here
TWILIO_AUTH_TOKEN=your_twilio_token_here
TWILIO_PHONE_NUMBER=your_twilio_number_here
```

## 📦 Dependencies

```
requests>=2.31.0
python-dotenv>=1.0.0
pandas>=2.0.0
matplotlib>=3.7.0
tabulate>=0.9.0
colorama>=0.4.6
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

## 🎓 Learning Objectives

- **HTTP Methods**: GET, POST, PUT, DELETE
- **Authentication**: API keys, Bearer tokens, OAuth
- **Headers**: Setting custom headers, user agents
- **Query Parameters**: Building URLs with parameters
- **Response Handling**: JSON parsing, error codes
- **Rate Limiting**: Handling API limits gracefully
- **Async Requests**: Concurrent API calls (advanced)
- **Environment Variables**: Secure credential management
- **Error Handling**: Try-except, retry logic
- **Data Processing**: Transforming API responses

## 📁 Project Structure

```
python-api-projects/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── 01-news-aggregator/
│   ├── aggregator.py
│   └── config.py
├── 02-weather-dashboard/
│   └── dashboard.py
├── 03-crypto-tracker/
│   └── tracker.py
├── 04-github-analytics/
│   └── analytics.py
├── 05-notification-system/
│   └── notifier.py
└── 06-multi-api-dashboard/
    └── dashboard.py
```

## 🔐 API Key Resources

### Free API Keys:

1. **NewsAPI**: https://newsapi.org/register
2. **OpenWeatherMap**: https://openweathermap.org/api
3. **CoinGecko**: No key needed
4. **GitHub**: https://github.com/settings/tokens
5. **SendGrid**: https://signup.sendgrid.com/
6. **Twilio**: https://www.twilio.com/try-twilio (trial credits)

### Tips:
- Never commit API keys to GitHub
- Use `.env` file for local development
- Use environment variables in production
- Rotate keys periodically
- Monitor usage to avoid exceeding limits

## 💡 Usage Examples

```bash
# News Aggregator
python 01-news-aggregator/aggregator.py --topic "technology" --sources 3

# Weather Dashboard
python 02-weather-dashboard/dashboard.py --city "London" --forecast 7

# Crypto Tracker
python 03-crypto-tracker/tracker.py --coins BTC ETH --alerts

# GitHub Analytics
python 04-github-analytics/analytics.py --repo "python/cpython"

# Send Notification
python 05-notification-system/notifier.py --email user@example.com --message "Hello"

# Multi-API Dashboard
python 06-multi-api-dashboard/dashboard.py --refresh 60
```

## 🛡️ Best Practices

1. **API Key Security**
   - Never hardcode API keys
   - Use environment variables
   - Add `.env` to `.gitignore`

2. **Rate Limiting**
   - Respect API rate limits
   - Implement exponential backoff
   - Cache responses when possible

3. **Error Handling**
   - Handle network errors gracefully
   - Check HTTP status codes
   - Provide meaningful error messages

4. **Data Validation**
   - Validate API responses
   - Handle missing data
   - Use try-except blocks

## 🔧 Troubleshooting

### Common Issues:

**"Invalid API Key"**
- Check if key is correctly set in `.env`
- Verify key is active on provider's website
- Check for extra spaces in the key

**"Rate Limit Exceeded"**
- Wait for the reset time
- Upgrade to paid tier if needed
- Implement caching

**"Connection Timeout"**
- Check internet connection
- Increase timeout value
- Verify API endpoint is correct

## 🤝 Contributing

Contributions are welcome! Ideas for new projects:
- Stock market tracker
- Social media API integrations
- Translation service
- Music API integration (Spotify)
- Movie database (TMDB)

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

Frank Bwalya -https://github.com/b5119

## 🌟 Acknowledgments

- NewsAPI for news data
- OpenWeatherMap for weather data
- CoinGecko for crypto data
- GitHub for repository data
- SendGrid & Twilio for notifications

---

⭐ **If you find this repository helpful, please star it!**

## 📊 API Comparison Table

| Project | APIs Used | Free Tier | Auth Method | Difficulty |
|---------|-----------|-----------|-------------|------------|
| News Aggregator | NewsAPI, Guardian | Yes | API Key | ⭐ Beginner |
| Weather Dashboard | OpenWeatherMap | Yes | API Key | ⭐⭐ Intermediate |
| Crypto Tracker | CoinGecko, Binance | Yes | API Key/None | ⭐⭐ Intermediate |
| GitHub Analytics | GitHub API | Yes | Token | ⭐⭐ Intermediate |
| Notification System | SendGrid, Twilio | Trial | API Key | ⭐⭐⭐ Advanced |
| Multi-API Dashboard | Multiple | Varies | Various | ⭐⭐⭐ Advanced |
