from datetime import datetime
import json
import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ThreatAnalysis(Base):
    __tablename__ = 'threat_analyses'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    query = Column(String, nullable=False)
    response = Column(JSON, nullable=False)
    tags = Column(JSON, nullable=False)

class Database:
    def __init__(self):
        self.engine = create_engine(os.environ['DATABASE_URL'])
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def store_analysis(self, query, response, tags):
        analysis = ThreatAnalysis(
            query=query,
            response=response,
            tags=tags
        )
        self.session.add(analysis)
        self.session.commit()
        return self._to_dict(analysis)
    
    def get_all_analyses(self):
        analyses = self.session.query(ThreatAnalysis).all()
        return [self._to_dict(analysis) for analysis in analyses]
    
    def to_dataframe(self):
        analyses = self.get_all_analyses()
        return pd.DataFrame(analyses)
    
    def export_analysis(self, format='csv'):
        df = self.to_dataframe()
        if format == 'csv':
            return df.to_csv(index=False)
        elif format == 'json':
            return df.to_json(orient='records')
        return None
    
    def _to_dict(self, analysis):
        return {
            'timestamp': analysis.timestamp.isoformat(),
            'query': analysis.query,
            'response': analysis.response,
            'tags': analysis.tags
        }
