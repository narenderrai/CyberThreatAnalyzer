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

    def generate_threat_report(self, analysis_data):
        """Generate a formatted threat analysis report."""
        
        report = []
        report.append("📊 THREAT ANALYSIS REPORT")
        report.append("=" * 50)

        # Process API Response
        if 'api_response' in analysis_data:
            api_data = analysis_data['api_response']
            
            if isinstance(api_data, dict) and 'data' in api_data:
                data = api_data['data']
                
                if 'attack_vector' in data:
                    report.append("\n🎯 Attack Vector Analysis")
                    report.append("-" * 30)
                    vectors = data['attack_vector'].replace('\\boxed{', '').replace('}', '').split(". ")
                    report.extend([f"• {v.strip()}" for v in vectors if v.strip()])

                if 'timeline' in data:
                    report.append("\n⏱️ Attack Timeline")
                    report.append("-" * 30)
                    timeline = data['timeline'].replace('\\boxed{', '').replace('}', '').split(". ")
                    report.extend([f"{i}. {step.strip()}" for i, step in enumerate(timeline, 1) if step.strip()])

                if 'impact' in data:
                    report.append("\n💥 Potential Impact")
                    report.append("-" * 30)
                    impacts = data['impact'].replace('\\boxed{', '').replace('}', '').split(".")
                    report.extend([f"• {imp.strip()}" for imp in impacts if imp.strip()])

                if 'mitigation' in data:
                    report.append("\n🛡️ Recommended Mitigations")
                    report.append("-" * 30)
                    mitigations = data['mitigation'].replace('\\boxed{', '').replace('}', '').split(". ")
                    report.extend([f"{i}. {mit.strip()}" for i, mit in enumerate(mitigations, 1) if mit.strip()])

        # Process Scraped Data
        if 'scraped_data' in analysis_data:
            scraped = analysis_data['scraped_data']
            
            if scraped.get('cve_data'):
                report.append("\n🔍 Related CVEs")
                report.append("-" * 30)
                report.extend([f"• {cve}" for cve in scraped['cve_data']])
            
            if scraped.get('exploit_data'):
                report.append("\n⚠️ Related Exploits")
                report.append("-" * 30)
                report.extend([f"• {exploit}" for exploit in scraped['exploit_data']])

        if not report[2:]:  # Check if there's any content beyond the header
            report.append("\nNo threat analysis data available.")

        return "\n".join(report)