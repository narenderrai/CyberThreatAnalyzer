from datetime import datetime
import json
import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool  # Change to NullPool for better SSL handling

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
        self.initialize_connection()

    def initialize_connection(self):
        if 'DATABASE_URL' not in os.environ:
            raise EnvironmentError("DATABASE_URL environment variable is not set. Please enable the database in Replit's Database tool.")
            
        retries = 3
        delay = 2  # seconds between retries
        while retries > 0:
            try:
                self.engine = create_engine(
                    os.environ['DATABASE_URL'],
                    poolclass=NullPool,
                    connect_args={
                        'sslmode': 'require',
                        'connect_timeout': 30,
                        'keepalives': 1,
                        'keepalives_idle': 30,
                        'keepalives_interval': 10,
                        'keepalives_count': 5
                    }
                )
                # Test the connection
                with self.engine.connect() as conn:
                    conn.execute("SELECT 1")
                Base.metadata.create_all(self.engine)
                session_factory = sessionmaker(bind=self.engine)
                self.Session = scoped_session(session_factory)
                print("Database connection established successfully")
                return
            except Exception as e:
                retries -= 1
                if retries == 0:
                    print(f"Database connection failed after 3 attempts: {str(e)}")
                    print("Please ensure your database is enabled in the Replit Database tab")
                    raise
                print(f"Connection attempt failed, retrying... ({retries} attempts remaining)")
                import time
                time.sleep(2)

    def store_analysis(self, query, response, tags):
        session = self.Session()
        try:
            analysis = ThreatAnalysis(
                query=query,
                response=response,
                tags=tags
            )
            session.add(analysis)
            session.commit()
            result = self._to_dict(analysis)
            return result
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def get_all_analyses(self):
        session = self.Session()
        try:
            analyses = session.query(ThreatAnalysis).all()
            return [self._to_dict(analysis) for analysis in analyses]
        finally:
            session.close()

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