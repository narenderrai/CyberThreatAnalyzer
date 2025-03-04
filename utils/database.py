
from datetime import datetime
import json
import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool

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
            print("WARNING: DATABASE_URL not found. Using SQLite file database for testing.")
            # Use a file-based SQLite database instead of in-memory
            self.engine = create_engine('sqlite:///threat_database.db')
            
            # Make sure the ThreatAnalysis table is created
            Base.metadata.create_all(self.engine)
            session_factory = sessionmaker(bind=self.engine)
            self.Session = scoped_session(session_factory)
            
            # Verify tables are created
            from sqlalchemy import inspect
            inspector = inspect(self.engine)
            tables = inspector.get_table_names()
            print(f"Created tables: {tables}")
            
            if 'threat_analyses' not in tables:
                print("Forcing table creation for ThreatAnalysis")
                ThreatAnalysis.__table__.create(self.engine, checkfirst=True)
                
                # Verify tables again after forcing creation
                tables = inspector.get_table_names()
                print(f"Tables after forced creation: {tables}")
            return
            
        retries = 3
        while retries > 0:
            try:
                self.engine = create_engine(
                    os.environ['DATABASE_URL'],
                    poolclass=QueuePool,
                    pool_size=5,
                    max_overflow=10,
                    pool_timeout=30,
                    pool_recycle=1800,
                    connect_args={'sslmode': 'require'}
                )
                
                # Test connection and create tables
                Base.metadata.create_all(self.engine)
                session_factory = sessionmaker(bind=self.engine)
                self.Session = scoped_session(session_factory)
                return
            except Exception as e:
                retries -= 1
                if retries == 0:
                    print(f"Database connection failed after 3 attempts: {str(e)}")
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
