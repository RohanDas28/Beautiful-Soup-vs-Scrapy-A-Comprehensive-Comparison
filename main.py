# Examples of Beautiful Soup and Scrapy Usage
# This file demonstrates practical examples of web scraping using both Beautiful Soup and Scrapy

# ===== Beautiful Soup Examples =====
from bs4 import BeautifulSoup
import requests
import json
from typing import List, Dict
import time

def beautiful_soup_example():
    """
    Demonstrates basic and advanced Beautiful Soup usage with error handling
    and practical data extraction examples.
    """
    print("\n=== Beautiful Soup Examples ===")
    
    # Example 1: Basic HTML Parsing
    print("\nExample 1: Basic HTML Parsing")
    try:
        url = "https://example.com"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract all links with their text
        print("\nAll Links:")
        for link in soup.find_all('a'):
            href = link.get('href')
            text = link.text.strip()
            if href and text:
                print(f"Link: {href} | Text: {text}")
        
        # Extract all headings
        print("\nAll Headings:")
        for heading in soup.find_all(['h1', 'h2', 'h3']):
            print(f"{heading.name}: {heading.text.strip()}")
            
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")

    # Example 2: Advanced Data Extraction
    print("\nExample 2: Advanced Data Extraction")
    try:
        # Using a more complex example site
        url = "https://quotes.toscrape.com"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract quotes with authors and tags
        quotes_data = []
        for quote in soup.find_all('div', class_='quote'):
            quote_data = {
                'text': quote.find('span', class_='text').text,
                'author': quote.find('small', class_='author').text,
                'tags': [tag.text for tag in quote.find_all('a', class_='tag')]
            }
            quotes_data.append(quote_data)
        
        # Save to JSON file
        with open('quotes.json', 'w', encoding='utf-8') as f:
            json.dump(quotes_data, f, indent=4, ensure_ascii=False)
        print("Quotes data saved to quotes.json")
        
    except Exception as e:
        print(f"Error in advanced example: {e}")

# ===== Scrapy Examples =====
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
from scrapy.exporters import JsonItemExporter

class QuotesSpider(scrapy.Spider):
    """
    A Scrapy spider that crawls quotes.toscrape.com and extracts quotes,
    authors, and tags.
    """
    name = 'quotes'
    start_urls = ['https://quotes.toscrape.com']
    
    def parse(self, response):
        """
        Parse the main page and extract quotes.
        """
        # Extract quotes from current page
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('a.tag::text').getall()
            }
        
        # Follow pagination links
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

class AdvancedSpider(scrapy.Spider):
    """
    An advanced Scrapy spider that demonstrates more complex scraping patterns
    including following author links and handling multiple item types.
    """
    name = 'advanced'
    start_urls = ['https://quotes.toscrape.com']
    
    def parse(self, response):
        """
        Parse the main page and follow both quote and author links.
        """
        # Extract quotes
        for quote in response.css('div.quote'):
            quote_data = {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('a.tag::text').getall()
            }
            yield quote_data
            
            # Follow author links
            author_url = quote.css('small.author + a::attr(href)').get()
            if author_url:
                yield response.follow(author_url, self.parse_author)
        
        # Follow pagination
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
    
    def parse_author(self, response):
        """
        Parse author pages to extract detailed information.
        """
        yield {
            'name': response.css('h3.author-title::text').get(),
            'birth_date': response.css('span.author-born-date::text').get(),
            'birth_location': response.css('span.author-born-location::text').get(),
            'description': response.css('div.author-description::text').get().strip()
        }

def scrapy_example():
    """
    Run Scrapy spiders with different configurations.
    """
    print("\n=== Scrapy Examples ===")
    
    # Basic example
    print("\nRunning basic quotes spider...")
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'quotes.json',
        'LOG_LEVEL': 'INFO',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    process.crawl(QuotesSpider)
    process.start()
    
    # Advanced example
    print("\nRunning advanced spider...")
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'advanced_data.json',
        'LOG_LEVEL': 'INFO',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 1
    })
    process.crawl(AdvancedSpider)
    process.start()

if __name__ == "__main__":
    # Run Beautiful Soup examples
    print("Running Beautiful Soup examples:")
    beautiful_soup_example()
    
    # Run Scrapy examples
    print("\nRunning Scrapy examples:")
    scrapy_example() 