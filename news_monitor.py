import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import re

# Keywords to search for
KEYWORDS = [
    "elon musk", "tesla", "tesla stock", "Tesla Inc", "Tesla, Inc", "SpaceX", 
    "X", "Boring Company", "xAI", "Neuralink", "OpenAI", "AI", "artificial intelligence",
]

# News sources to monitor
NEWS_SOURCES = [
    "https://www.reuters.com",
    "https://www.bloomberg.com",
    "https://www.cnbc.com",
    "https://www.bbc.com/news",
    "https://www.theguardian.com/international"
]

def check_news_site(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        return None

def find_articles(html_content, source_url):
    if not html_content:
        return []
    
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = []
    
    # Find all links in the page
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        text = link.get_text().lower()
        
        # Check if the link contains any of our keywords
        if any(keyword.lower() in text for keyword in KEYWORDS):
            # Make sure the URL is absolute
            if not href.startswith('http'):
                if href.startswith('/'):
                    href = source_url + href
                else:
                    href = source_url + '/' + href
            
            articles.append(href)
    
    return articles

def save_articles(articles):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"elon_news_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Articles found at {timestamp}\n\n")
        for article in articles:
            f.write(f"{article}\n")
    
    print(f"Saved {len(articles)} articles to {filename}")

def main():
    all_articles = set()  # Using set to avoid duplicates
    
    for source in NEWS_SOURCES:
        print(f"Checking {source}...")
        html_content = check_news_site(source)
        if html_content:
            articles = find_articles(html_content, source)
            all_articles.update(articles)
            print(f"Found {len(articles)} articles on {source}")
        
        # Be nice to the servers
        time.sleep(2)
    
    if all_articles:
        save_articles(all_articles)
    else:
        print("No articles found matching the criteria.")

if __name__ == "__main__":
    main() 