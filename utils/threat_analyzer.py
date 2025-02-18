import pandas as pd
from datetime import datetime

class ThreatAnalyzer:
    def __init__(self):
        self.responses = []
        
    def store_response(self, query, response, tags):
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response,
            'tags': tags
        }
        self.responses.append(analysis)
        return analysis

    def get_historical_analysis(self):
        return pd.DataFrame(self.responses)

    def export_analysis(self, format='csv'):
        df = self.get_historical_analysis()
        if format == 'csv':
            return df.to_csv(index=False)
        elif format == 'json':
            return df.to_json(orient='records')
        return None
