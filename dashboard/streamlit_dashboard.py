"""
Interactive Data Centralization Platform Dashboard

A comprehensive Streamlit dashboard for exploring cross-domain correlations,
semantic search, and business insights in real-time.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import asyncio
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.correlation_analysis_demo import CorrelationAnalysisDemo

# Try to import LLM services, fall back to mock if not available
try:
    from packages.shared_core.shared_core.embeddings.embedding_service import EmbeddingService
    from packages.shared_core.shared_core.llm.rag_system import CorrelationRAGSystem
    LLM_AVAILABLE = True
except ImportError:
    # Mock services for dashboard demo without full LLM setup
    class MockEmbeddingService:
        def __init__(self):
            pass
        async def generate_embeddings_batch(self, texts):
            return [[0.1] * 384 for _ in texts]
    
    class MockRAGSystem:
        def __init__(self):
            pass
        async def query_correlations(self, query):
            return type('MockResponse', (), {
                'answer': f'This is a mock response for: {query}. The system would analyze correlations and provide insights.',
                'confidence': 0.85
            })()
    
    EmbeddingService = MockEmbeddingService
    CorrelationRAGSystem = MockRAGSystem
    LLM_AVAILABLE = False


# Page configuration
st.set_page_config(
    page_title="Data Centralization Platform",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_demo_data():
    """Load and cache demo data for the dashboard"""
    demo = CorrelationAnalysisDemo()
    return demo


@st.cache_data
def calculate_correlations():
    """Calculate and cache correlation results"""
    demo = load_demo_data()
    cross_correlations = demo.calculate_cross_domain_correlations()
    temporal_correlations = demo.calculate_temporal_correlations()
    entity_links = demo.run_entity_linking_demo()
    summary = demo.generate_summary_report()
    
    return cross_correlations, temporal_correlations, entity_links, summary


def create_correlation_heatmap(demo):
    """Create interactive correlation heatmap"""
    # Create a combined correlation matrix
    combined_data = pd.DataFrame({
        'music_valence': demo.demo_data['music']['valence'],
        'music_energy': demo.demo_data['music']['energy'],
        'weather_temp': demo.demo_data['weather']['temperature'],
        'weather_humidity': demo.demo_data['weather']['humidity'],
        'movie_revenue': demo.demo_data['movies']['box_office_revenue'],
        'soundtrack_pop': demo.demo_data['movies']['soundtrack_popularity'],
        'pokemon_popularity': demo.demo_data['pokemon']['popularity_score'],
        'github_stars': demo.demo_data['repositories']['stars_count']
    })
    
    correlation_matrix = combined_data.corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.index,
        colorscale='RdBu',
        zmid=0,
        hoverongaps=False,
        hovertemplate='<b>%{y}</b> vs <b>%{x}</b><br>' +
                     'Correlation: %{z:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Cross-Domain Correlation Matrix",
        xaxis_title="Variables",
        yaxis_title="Variables",
        width=800,
        height=600,
        font=dict(size=10)
    )
    
    return fig


def create_time_series_chart(demo):
    """Create time series visualization"""
    ts_data = demo.demo_data['time_series']
    
    fig = go.Figure()
    
    # Add traces for different metrics
    fig.add_trace(go.Scatter(
        x=ts_data['date'],
        y=ts_data['music_streams'],
        mode='lines',
        name='Music Streams',
        line=dict(color='#1f77b4')
    ))
    
    # Add secondary y-axis for temperature
    fig.add_trace(go.Scatter(
        x=ts_data['date'],
        y=ts_data['avg_temperature'],
        mode='lines',
        name='Avg Temperature',
        yaxis='y2',
        line=dict(color='#ff7f0e')
    ))
    
    fig.update_layout(
        title="Temporal Patterns: Music Streams vs Temperature",
        xaxis_title="Date",
        yaxis=dict(title="Music Streams", side="left"),
        yaxis2=dict(title="Temperature (°C)", side="right", overlaying="y"),
        hovermode='x unified',
        width=800,
        height=400
    )
    
    return fig


def create_domain_distribution_chart(demo):
    """Create domain distribution pie chart"""
    domain_counts = {
        'Music': len(demo.demo_data['music']),
        'Weather': len(demo.demo_data['weather']),
        'Movies': len(demo.demo_data['movies']),
        'Pokemon': len(demo.demo_data['pokemon']),
        'Repositories': len(demo.demo_data['repositories'])
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=list(domain_counts.keys()),
        values=list(domain_counts.values()),
        hole=0.3
    )])
    
    fig.update_layout(
        title="Data Distribution Across Domains",
        width=400,
        height=400
    )
    
    return fig


def main():
    """Main dashboard application"""
    
    # Header
    st.markdown('<div class="main-header">🔗 Data Centralization Platform</div>', 
                unsafe_allow_html=True)
    st.markdown("### Cross-Domain Correlation Analysis & Semantic Search")
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Overview", "Correlation Analysis", "Semantic Search", "Business Insights", "Raw Data"]
    )
    
    # Load data
    demo = load_demo_data()
    cross_correlations, temporal_correlations, entity_links, summary = calculate_correlations()
    
    if page == "Overview":
        st.header("📊 Platform Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.metric("Total Records", summary['data_summary']['total_records'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.metric("Domains Analyzed", summary['data_summary']['total_domains'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.metric("Significant Correlations", summary['correlation_analysis']['significant_correlations'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.metric("Significance Rate", f"{summary['correlation_analysis']['significant_rate']:.1%}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_correlation_heatmap(demo), use_container_width=True)
        
        with col2:
            st.plotly_chart(create_domain_distribution_chart(demo), use_container_width=True)
        
        # Time series
        st.plotly_chart(create_time_series_chart(demo), use_container_width=True)
        
        # Business insights
        st.header("🎯 Key Business Insights")
        for insight in summary['business_insights']:
            st.markdown(f'<div class="insight-box">💡 {insight}</div>', unsafe_allow_html=True)
    
    elif page == "Correlation Analysis":
        st.header("📈 Correlation Analysis")
        
        # Correlation results
        st.subheader("Cross-Domain Correlations")
        
        correlation_df = pd.DataFrame(cross_correlations + temporal_correlations)
        
        # Filter controls
        col1, col2 = st.columns(2)
        with col1:
            significance_filter = st.selectbox(
                "Filter by significance:",
                ["All", "Significant Only", "Non-significant Only"]
            )
        with col2:
            strength_threshold = st.slider(
                "Minimum correlation strength:",
                0.0, 1.0, 0.3, 0.05
            )
        
        # Apply filters
        filtered_df = correlation_df.copy()
        
        if significance_filter == "Significant Only":
            filtered_df = filtered_df[filtered_df['p_value'] < 0.05]
        elif significance_filter == "Non-significant Only":
            filtered_df = filtered_df[filtered_df['p_value'] >= 0.05]
        
        filtered_df = filtered_df[
            filtered_df['correlation_coefficient'].abs() >= strength_threshold
        ]
        
        # Display results
        if not filtered_df.empty:
            st.dataframe(
                filtered_df[['domain1', 'domain2', 'variable1', 'variable2', 
                           'correlation_coefficient', 'p_value', 'method']],
                use_container_width=True
            )
            
            # Visualization
            st.plotly_chart(create_correlation_heatmap(demo), use_container_width=True)
        else:
            st.warning("No correlations match the selected criteria.")
    
    elif page == "Semantic Search":
        st.header("🔍 Semantic Search")
        
        # Note about API key requirement
        st.info("💡 Semantic search requires OpenAI API key. This is a demo interface.")
        
        # Search interface
        search_query = st.text_input(
            "Enter your search query:",
            placeholder="e.g., 'upbeat energetic music' or 'rainy weather patterns'"
        )
        
        domain_filter = st.selectbox(
            "Filter by domain (optional):",
            ["All Domains", "music", "weather", "entertainment", "gaming", "development", "productivity"]
        )
        
        if st.button("Search", type="primary"):
            if search_query:
                # Simulate search results (since we don't have live API)
                st.subheader("Search Results")
                
                # Mock results
                mock_results = [
                    {
                        "entity_type": "Track",
                        "content": "Hymn for the Weekend Coldplay upbeat dance energetic",
                        "domain": "music",
                        "similarity": 0.89
                    },
                    {
                        "entity_type": "Movie",
                        "content": "Thor Ragnarok Marvel superhero action adventure comedy",
                        "domain": "entertainment",
                        "similarity": 0.76
                    },
                    {
                        "entity_type": "Weather",
                        "content": "clear hot weather sunny conditions 28°C",
                        "domain": "weather",
                        "similarity": 0.65
                    }
                ]
                
                for i, result in enumerate(mock_results, 1):
                    st.markdown(f"""
                    **{i}. [{result['entity_type']}] {result['content']}**  
                    Domain: {result['domain']} | Similarity: {result['similarity']:.3f}
                    """)
            else:
                st.warning("Please enter a search query.")
    
    elif page == "Business Insights":
        st.header("💼 Business Intelligence")
        
        # Top correlations
        st.subheader("Most Significant Correlations")
        
        significant_correlations = [
            corr for corr in cross_correlations + temporal_correlations 
            if corr['p_value'] < 0.05
        ]
        
        if significant_correlations:
            sorted_correlations = sorted(
                significant_correlations,
                key=lambda x: abs(x['correlation_coefficient']),
                reverse=True
            )
            
            for i, corr in enumerate(sorted_correlations[:5], 1):
                strength = corr['interpretation']['strength']
                direction = corr['interpretation']['direction']
                relevance = corr['interpretation']['business_relevance']
                
                st.markdown(f"""
                **{i}. {corr['domain1'].title()} ↔ {corr['domain2'].title()}**
                - Variables: {corr['variable1']} vs {corr['variable2']}
                - Correlation: {corr['correlation_coefficient']:.3f} ({strength} {direction})
                - P-value: {corr['p_value']:.3f}
                - Business Relevance: {relevance}
                """)
        
        # Business insights
        st.subheader("Actionable Insights")
        for insight in summary['business_insights']:
            st.markdown(f'<div class="insight-box">🎯 {insight}</div>', unsafe_allow_html=True)
        
        # Entity linking results
        st.subheader("Cross-Domain Entity Links")
        
        for link_type, links in entity_links.items():
            st.markdown(f"**{link_type.replace('_', ' ').title()}:**")
            for link in links:
                st.json(link)
    
    elif page == "Raw Data":
        st.header("📋 Raw Data Explorer")
        
        # Domain selector
        selected_domain = st.selectbox(
            "Select domain to explore:",
            ["music", "weather", "movies", "pokemon", "repositories", "time_series"]
        )
        
        if selected_domain in demo.demo_data:
            data = demo.demo_data[selected_domain]
            
            st.subheader(f"{selected_domain.title()} Data")
            st.write(f"Total records: {len(data)}")
            
            # Display data
            if isinstance(data, pd.DataFrame):
                st.dataframe(data, use_container_width=True)
                
                # Basic statistics
                if st.checkbox("Show statistics"):
                    st.subheader("Statistical Summary")
                    st.write(data.describe())
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
    🔗 Data Centralization Platform | Proof of Concept Dashboard<br>
    Built with Streamlit, Plotly, and advanced correlation analysis
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
