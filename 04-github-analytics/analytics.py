#!/usr/bin/env python3
"""
GitHub Repository Analytics
Analyze GitHub repositories with detailed statistics
API: GitHub REST API
"""

import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import json
import argparse
from collections import Counter

# Load environment variables
load_dotenv()

class GitHubAnalytics:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.base_url = 'https://api.github.com'
        self.headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'
            print("✅ Using authenticated requests")
        else:
            print("⚠️  No GitHub token found (60 requests/hour limit)")
            print("Create token at: https://github.com/settings/tokens")
    
    def check_rate_limit(self):
        """Check API rate limit status"""
        endpoint = f"{self.base_url}/rate_limit"
        
        try:
            response = requests.get(endpoint, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            core = data['rate']
            
            print(f"\n📊 API Rate Limit:")
            print(f"   Remaining: {core['remaining']}/{core['limit']}")
            print(f"   Resets at: {datetime.fromtimestamp(core['reset']).strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            return core['remaining']
            
        except Exception as e:
            print(f"❌ Error checking rate limit: {e}")
            return None
    
    def get_repository(self, owner, repo):
        """Get repository information"""
        endpoint = f"{self.base_url}/repos/{owner}/{repo}"
        
        try:
            print(f"📦 Fetching repository: {owner}/{repo}...")
            response = requests.get(endpoint, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"❌ Repository '{owner}/{repo}' not found!")
            else:
                print(f"❌ HTTP Error: {e}")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def get_contributors(self, owner, repo, limit=100):
        """Get repository contributors"""
        endpoint = f"{self.base_url}/repos/{owner}/{repo}/contributors"
        params = {'per_page': limit}
        
        try:
            print(f"👥 Fetching contributors...")
            response = requests.get(endpoint, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"❌ Error fetching contributors: {e}")
            return []
    
    def get_languages(self, owner, repo):
        """Get programming languages used"""
        endpoint = f"{self.base_url}/repos/{owner}/{repo}/languages"
        
        try:
            print(f"💻 Fetching languages...")
            response = requests.get(endpoint, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"❌ Error fetching languages: {e}")
            return {}
    
    def get_commits(self, owner, repo, since=None, until=None, limit=100):
        """Get commit history"""
        endpoint = f"{self.base_url}/repos/{owner}/{repo}/commits"
        params = {'per_page': limit}
        
        if since:
            params['since'] = since
        if until:
            params['until'] = until
        
        try:
            print(f"📝 Fetching commits...")
            response = requests.get(endpoint, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"❌ Error fetching commits: {e}")
            return []
    
    def get_issues(self, owner, repo, state='all', limit=100):
        """Get repository issues"""
        endpoint = f"{self.base_url}/repos/{owner}/{repo}/issues"
        params = {
            'state': state,
            'per_page': limit
        }
        
        try:
            print(f"🐛 Fetching issues...")
            response = requests.get(endpoint, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            # Filter out pull requests
            issues = [item for item in response.json() if 'pull_request' not in item]
            return issues
            
        except Exception as e:
            print(f"❌ Error fetching issues: {e}")
            return []
    
    def get_pull_requests(self, owner, repo, state='all', limit=100):
        """Get pull requests"""
        endpoint = f"{self.base_url}/repos/{owner}/{repo}/pulls"
        params = {
            'state': state,
            'per_page': limit
        }
        
        try:
            print(f"🔀 Fetching pull requests...")
            response = requests.get(endpoint, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"❌ Error fetching pull requests: {e}")
            return []
    
    def get_releases(self, owner, repo):
        """Get repository releases"""
        endpoint = f"{self.base_url}/repos/{owner}/{repo}/releases"
        
        try:
            print(f"🏷️  Fetching releases...")
            response = requests.get(endpoint, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"❌ Error fetching releases: {e}")
            return []
    
    def get_traffic_views(self, owner, repo):
        """Get repository traffic views (requires push access)"""
        endpoint = f"{self.base_url}/repos/{owner}/{repo}/traffic/views"
        
        try:
            response = requests.get(endpoint, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            # Traffic data requires push access
            return None
    
    def display_repository_info(self, repo_data):
        """Display repository information"""
        if not repo_data:
            return
        
        print(f"\n{'='*100}")
        print(f"📦 REPOSITORY: {repo_data['full_name']}")
        print(f"{'='*100}\n")
        
        print(f"📝 Description: {repo_data.get('description', 'No description')}")
        print(f"🔗 URL: {repo_data['html_url']}")
        print(f"👤 Owner: {repo_data['owner']['login']}")
        
        print(f"\n📊 Statistics:")
        print(f"   ⭐ Stars: {repo_data['stargazers_count']:,}")
        print(f"   👁️  Watchers: {repo_data['watchers_count']:,}")
        print(f"   🔱 Forks: {repo_data['forks_count']:,}")
        print(f"   🐛 Open Issues: {repo_data['open_issues_count']:,}")
        print(f"   💾 Size: {repo_data['size']:,} KB")
        
        print(f"\n📅 Dates:")
        created = datetime.strptime(repo_data['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        updated = datetime.strptime(repo_data['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
        print(f"   Created: {created.strftime('%Y-%m-%d')}")
        print(f"   Updated: {updated.strftime('%Y-%m-%d')}")
        
        print(f"\n🏷️  Info:")
        print(f"   Default Branch: {repo_data['default_branch']}")
        print(f"   License: {repo_data['license']['name'] if repo_data.get('license') else 'No license'}")
        print(f"   Language: {repo_data.get('language', 'Not specified')}")
        
        if repo_data.get('topics'):
            print(f"   Topics: {', '.join(repo_data['topics'])}")
        
        print(f"{'='*100}\n")
    
    def display_contributors(self, contributors, limit=10):
        """Display top contributors"""
        if not contributors:
            return
        
        print(f"\n{'='*80}")
        print(f"👥 TOP CONTRIBUTORS")
        print(f"{'='*80}\n")
        
        print(f"{'Username':<30} {'Contributions':<15} {'Profile'}")
        print("-" * 80)
        
        for contrib in contributors[:limit]:
            username = contrib['login']
            contributions = contrib['contributions']
            profile_url = contrib['html_url']
            
            print(f"{username:<30} {contributions:<15,} {profile_url}")
        
        print(f"{'='*80}\n")
    
    def display_languages(self, languages):
        """Display language breakdown"""
        if not languages:
            return
        
        total_bytes = sum(languages.values())
        
        print(f"\n{'='*80}")
        print(f"💻 PROGRAMMING LANGUAGES")
        print(f"{'='*80}\n")
        
        print(f"{'Language':<20} {'Bytes':<15} {'Percentage':<15} {'Bar'}")
        print("-" * 80)
        
        sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
        
        for lang, bytes_count in sorted_langs:
            percentage = (bytes_count / total_bytes) * 100
            bar = '█' * int(percentage / 2)
            
            print(f"{lang:<20} {bytes_count:<15,} {percentage:>5.1f}%          {bar}")
        
        print(f"{'='*80}\n")
    
    def display_commit_stats(self, commits):
        """Display commit statistics"""
        if not commits:
            return
        
        print(f"\n{'='*80}")
        print(f"📝 COMMIT STATISTICS")
        print(f"{'='*80}\n")
        
        # Analyze commits
        authors = Counter()
        dates = Counter()
        
        for commit in commits:
            author = commit['commit']['author']['name']
            date = commit['commit']['author']['date'][:10]  # YYYY-MM-DD
            
            authors[author] += 1
            dates[date] += 1
        
        # Top authors
        print("🏆 Top 10 Committers:")
        for author, count in authors.most_common(10):
            print(f"   {author:<30} {count:>4} commits")
        
        # Recent activity
        print(f"\n📅 Recent Commit Activity:")
        for date, count in sorted(dates.items(), reverse=True)[:7]:
            bar = '█' * count
            print(f"   {date}: {count:>3} commits {bar}")
        
        # Recent commits
        print(f"\n📋 Latest 5 Commits:")
        for commit in commits[:5]:
            sha = commit['sha'][:7]
            author = commit['commit']['author']['name']
            message = commit['commit']['message'].split('\n')[0][:60]
            date = commit['commit']['author']['date'][:10]
            
            print(f"   {sha} - {author} ({date})")
            print(f"   {message}\n")
        
        print(f"{'='*80}\n")
    
    def display_issues_stats(self, issues):
        """Display issues statistics"""
        if not issues:
            print("\n✨ No issues found!\n")
            return
        
        open_issues = [i for i in issues if i['state'] == 'open']
        closed_issues = [i for i in issues if i['state'] == 'closed']
        
        print(f"\n{'='*80}")
        print(f"🐛 ISSUES STATISTICS")
        print(f"{'='*80}\n")
        
        print(f"Total Issues: {len(issues)}")
        print(f"Open: {len(open_issues)} | Closed: {len(closed_issues)}")
        
        # Label analysis
        labels = Counter()
        for issue in issues:
            for label in issue.get('labels', []):
                labels[label['name']] += 1
        
        if labels:
            print(f"\n🏷️  Top Labels:")
            for label, count in labels.most_common(10):
                print(f"   {label:<30} {count:>3}")
        
        # Recent open issues
        if open_issues:
            print(f"\n📌 Recent Open Issues:")
            for issue in open_issues[:5]:
                print(f"   #{issue['number']}: {issue['title'][:60]}")
                print(f"   Created: {issue['created_at'][:10]} | Comments: {issue['comments']}\n")
        
        print(f"{'='*80}\n")
    
    def display_releases(self, releases):
        """Display releases"""
        if not releases:
            print("\n📦 No releases found\n")
            return
        
        print(f"\n{'='*80}")
        print(f"🏷️  RELEASES")
        print(f"{'='*80}\n")
        
        for release in releases[:10]:
            tag = release['tag_name']
            name = release.get('name', tag)
            date = release['published_at'][:10]
            author = release['author']['login']
            
            print(f"📦 {name} ({tag})")
            print(f"   Published: {date} by {author}")
            print(f"   Downloads: {release.get('assets', []).__len__()} asset(s)")
            print()
        
        print(f"{'='*80}\n")
    
    def generate_full_report(self, owner, repo):
        """Generate comprehensive repository report"""
        print(f"\n{'#'*100}")
        print(f"# COMPREHENSIVE REPOSITORY ANALYSIS: {owner}/{repo}")
        print(f"{'#'*100}\n")
        
        # Get all data
        repo_data = self.get_repository(owner, repo)
        if not repo_data:
            return
        
        contributors = self.get_contributors(owner, repo)
        languages = self.get_languages(owner, repo)
        commits = self.get_commits(owner, repo, limit=100)
        issues = self.get_issues(owner, repo, limit=100)
        pull_requests = self.get_pull_requests(owner, repo, limit=50)
        releases = self.get_releases(owner, repo)
        
        # Display all information
        self.display_repository_info(repo_data)
        self.display_languages(languages)
        self.display_contributors(contributors, 10)
        self.display_commit_stats(commits)
        self.display_issues_stats(issues)
        self.display_releases(releases)
        
        # Summary
        print(f"\n{'='*80}")
        print(f"📊 SUMMARY")
        print(f"{'='*80}")
        print(f"Repository: {repo_data['full_name']}")
        print(f"Stars: {repo_data['stargazers_count']:,} | Forks: {repo_data['forks_count']:,}")
        print(f"Contributors: {len(contributors)}")
        print(f"Languages: {len(languages)}")
        print(f"Commits analyzed: {len(commits)}")
        print(f"Issues: {len(issues)} | Pull Requests: {len(pull_requests)}")
        print(f"Releases: {len(releases)}")
        print(f"{'='*80}\n")
    
    def save_report(self, owner, repo, filename=None):
        """Save comprehensive report to JSON"""
        if not filename:
            filename = f"{owner}_{repo}_analysis.json"
        
        print(f"💾 Generating report...")
        
        report = {
            'repository': self.get_repository(owner, repo),
            'contributors': self.get_contributors(owner, repo),
            'languages': self.get_languages(owner, repo),
            'commits': self.get_commits(owner, repo, limit=100),
            'issues': self.get_issues(owner, repo, limit=100),
            'pull_requests': self.get_pull_requests(owner, repo, limit=50),
            'releases': self.get_releases(owner, repo),
            'analyzed_at': datetime.now().isoformat()
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, default=str)
            
            print(f"✅ Report saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving report: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='GitHub Repository Analytics Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analytics.py --repo torvalds/linux
  python analytics.py --repo python/cpython --full-report
  python analytics.py --repo facebook/react --contributors
  python analytics.py --repo microsoft/vscode --save report.json
  python analytics.py --rate-limit
        """
    )
    
    parser.add_argument('--repo', metavar='OWNER/REPO', help='Repository (owner/repo)')
    parser.add_argument('--full-report', action='store_true', help='Generate full analysis')
    parser.add_argument('--contributors', action='store_true', help='Show contributors')
    parser.add_argument('--languages', action='store_true', help='Show languages')
    parser.add_argument('--commits', action='store_true', help='Show commit stats')
    parser.add_argument('--issues', action='store_true', help='Show issues')
    parser.add_argument('--releases', action='store_true', help='Show releases')
    parser.add_argument('--save', metavar='FILE', help='Save report to JSON')
    parser.add_argument('--rate-limit', action='store_true', help='Check rate limit')
    
    args = parser.parse_args()
    
    analytics = GitHubAnalytics()
    
    if args.rate_limit:
        analytics.check_rate_limit()
        return
    
    if not args.repo:
        print("❌ Please specify a repository with --repo OWNER/REPO")
        print("Use --help for more information")
        return
    
    try:
        owner, repo = args.repo.split('/')
    except ValueError:
        print("❌ Invalid format! Use: OWNER/REPO (e.g., torvalds/linux)")
        return
    
    if args.save:
        analytics.save_report(owner, repo, args.save)
        return
    
    if args.full_report:
        analytics.generate_full_report(owner, repo)
        return
    
    # Get basic repo info
    repo_data = analytics.get_repository(owner, repo)
    analytics.display_repository_info(repo_data)
    
    # Show specific sections if requested
    if args.contributors:
        contributors = analytics.get_contributors(owner, repo)
        analytics.display_contributors(contributors)
    
    if args.languages:
        languages = analytics.get_languages(owner, repo)
        analytics.display_languages(languages)
    
    if args.commits:
        commits = analytics.get_commits(owner, repo)
        analytics.display_commit_stats(commits)
    
    if args.issues:
        issues = analytics.get_issues(owner, repo)
        analytics.display_issues_stats(issues)
    
    if args.releases:
        releases = analytics.get_releases(owner, repo)
        analytics.display_releases(releases)


if __name__ == "__main__":
    main()