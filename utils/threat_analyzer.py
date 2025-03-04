from datetime import datetime
import pandas as pd
from .database import Database

class ThreatAnalyzer:
    def __init__(self):
        self.db = Database()

    def store_response(self, query, response, tags):
        try:
            return self.db.store_analysis(query, response, tags)
        except Exception as e:
            print(f"Error storing analysis: {str(e)}")
            # Return a fallback response to prevent app from crashing
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