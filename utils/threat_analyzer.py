from datetime import datetime
import pandas as pd
from .database import Database

class ThreatAnalyzer:
    def __init__(self):
        self.db = Database()

    def store_response(self, query, response, tags):
        return self.db.store_analysis(query, response, tags)

    def get_historical_analysis(self):
        return self.db.to_dataframe()

    def export_analysis(self, format='csv'):
        return self.db.export_analysis(format)