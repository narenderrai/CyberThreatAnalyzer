from datetime import datetime
import pandas as pd
from .database import Database

from bs4 import BeautifulSoup
import requests
from datetime import datetime

class ThreatAnalyzer:
    def __init__(self):
        self.db = Database()
        self.scrape_sources = {
            'cve': 'https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=',
            'exploitdb': 'https://www.exploit-db.com/search?q='
        }

    def scrape_threat_data(self, query):
        scraped_data = {}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        try:
            # Search CVE database
            cve_url = self.scrape_sources['cve'] + query.replace(' ', '+')
            response = requests.get(cve_url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                cve_items = soup.find_all('tr')[1:6]  # Get first 5 CVEs
                scraped_data['cve_data'] = [item.get_text(strip=True) for item in cve_items if item]

            # Search ExploitDB
            exploit_url = self.scrape_sources['exploitdb'] + query.replace(' ', '+')
            response = requests.get(exploit_url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                exploit_items = soup.find_all('div', class_='card')[:5]  # Get first 5 exploits
                scraped_data['exploit_data'] = [item.get_text(strip=True) for item in exploit_items if item]

        except Exception as e:
            print(f"Error scraping data: {str(e)}")
            scraped_data['error'] = str(e)

        return scraped_data

    def store_response(self, query, response, tags):
        try:
            # Get scraped data
            scraped_data = self.scrape_threat_data(query)
            
            # Combine API response with scraped data
            combined_response = {
                'api_response': response,
                'scraped_data': scraped_data
            }
            
            return self.db.store_analysis(query, combined_response, tags)
        except Exception as e:
            print(f"Error storing analysis: {str(e)}")
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'query': query,
                'response': response,
                'tags': tags,
                'error': str(e)
            }

    def get_historical_analysis(self):
        return self.db.to_dataframe()

    def export_analysis(self, format='csv'):
        return self.db.export_analysis(format)