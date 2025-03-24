import requests
from bs4 import BeautifulSoup
from trendapi import GoogleTrends
import openai
import os
import random


class ResearchAgent:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        self.trend_client = GoogleTrends(api_key=os.getenv("GOOGLE_TRENDS_KEY"))

    def get_trending_topics(self):
        try:
            trends = self.trend_client.get_daily_trends(country="US")
            hr_trends = [t for t in trends if 'hr' in t.lower() or 'human resources' in t.lower()]
            return hr_trends[:3]  # Return top 3 HR trends
        except:
            return ["Hybrid Work Models", "Employee Wellbeing", "DEI Initiatives"]

    def scrape_website(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'lxml')

            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer']):
                element.decompose()

            return ' '.join([p.get_text().strip() for p in soup.find_all('p')])
        except Exception as e:
            print(f"Scraping error: {e}")
            return ""

    def execute(self):
        print("🕸️ Gathering latest HR trends...")
        topics = self.get_trending_topics()
        selected_topic = topics[0] if topics else "Modern HR Practices"

        print(f"📚 Researching topic: {selected_topic}")
        sources = {
            'articles': [],
            'statistics': [],
            'quotes': []
        }

        # Scrape relevant sources
        sources['articles'].append(self.scrape_website(
            f"https://www.shrm.org/search/pages/default.aspx?k={selected_topic}"
        ))
        sources['articles'].append(self.scrape_website(
            f"https://hbr.org/search?term={selected_topic}"
        ))

        return {
            'primary_topic': selected_topic,
            'sources': sources,
            'keywords': list(set([selected_topic.lower(), "hr trends", "workplace strategy"]))
        }