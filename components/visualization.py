import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class ThreatVisualizer:
    @staticmethod
    def create_threat_timeline(df):
        # Create a copy of the dataframe
        df_plot = df.copy()
        
        # Convert timestamp to datetime if it's not already
        if not pd.api.types.is_datetime64_any_dtype(df_plot['timestamp']):
            df_plot['timestamp'] = pd.to_datetime(df_plot['timestamp'])
        
        # Add end time (timestamp + 1 day) for timeline visualization
        df_plot['end_time'] = df_plot['timestamp'] + pd.Timedelta(days=1)
        
        fig = px.timeline(
            df_plot,
            x_start='timestamp',
            x_end='end_time',
            y='query',
            color='tags',
            title='Threat Analysis Timeline'
        )
        return fig

    @staticmethod
    def create_threat_distribution(df):
        tag_counts = df['tags'].value_counts()
        fig = px.pie(
            values=tag_counts.values,
            names=tag_counts.index,
            title='Distribution of Threat Types'
        )
        return fig

    @staticmethod
    def create_severity_gauge(severity_level):
        severity_map = {
            'Low': 25,
            'Medium': 50,
            'High': 75,
            'Critical': 100
        }
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = severity_map.get(severity_level, 0),
            title = {'text': "Threat Severity"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkred"},
                'steps': [
                    {'range': [0, 25], 'color': "lightgreen"},
                    {'range': [25, 50], 'color': "yellow"},
                    {'range': [50, 75], 'color': "orange"},
                    {'range': [75, 100], 'color': "red"},
                ]
            }
        ))
        return fig
