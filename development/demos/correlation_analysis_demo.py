"""
Proof of Concept: Statistical Correlation Analysis Demo

This script demonstrates the core statistical correlation functionality
of the data centralization platform using sample data, without requiring
a database connection.
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta, date
from decimal import Decimal
from scipy.stats import pearsonr, spearmanr
from typing import Dict, List, Any, Tuple
import matplotlib.pyplot as plt
import seaborn as sns

class CorrelationAnalysisDemo:
    """
    Demonstrates correlation analysis across different data domains
    """
    
    def __init__(self):
        self.demo_data = {}
        self._generate_sample_data()
    
    def _generate_sample_data(self):
        """Generate realistic sample data for all domains"""
        np.random.seed(42)  # For reproducible results
        
        # Music data
        self.demo_data['music'] = pd.DataFrame({
            'track_id': range(1, 101),
            'valence': np.random.beta(2, 2, 100),  # Positivity measure 0-1
            'energy': np.random.beta(2, 3, 100),   # Energy level 0-1
            'danceability': np.random.beta(3, 2, 100),
            'tempo': np.random.normal(120, 30, 100).clip(60, 200),
            'popularity': np.random.exponential(20, 100).clip(0, 100),
            'release_year': np.random.choice(range(1990, 2024), 100),
            'genre': np.random.choice(['rock', 'pop', 'electronic', 'jazz', 'classical'], 100)
        })
        
        # Weather data (aligned with music for correlation)
        base_temp = 20 + 15 * self.demo_data['music']['valence']  # Warmer = more positive
        self.demo_data['weather'] = pd.DataFrame({
            'location_id': range(1, 101),
            'temperature': base_temp + np.random.normal(0, 5, 100),
            'humidity': np.random.uniform(30, 90, 100),
            'pressure': np.random.normal(1013, 15, 100),
            'weather_condition': np.random.choice(['clear', 'rain', 'clouds', 'snow'], 100),
            'comfort_index': np.random.uniform(0.3, 0.9, 100)
        })
        
        # Entertainment data
        box_office_base = 50000000 + 200000000 * self.demo_data['music']['popularity'] / 100
        self.demo_data['movies'] = pd.DataFrame({
            'movie_id': range(1, 101),
            'box_office_revenue': box_office_base + np.random.normal(0, 50000000, 100),
            'soundtrack_popularity': self.demo_data['music']['popularity'] * np.random.uniform(0.7, 1.3, 100),
            'vote_average': np.random.uniform(4.0, 9.5, 100),
            'release_year': np.random.choice(range(2000, 2024), 100),
            'genre': np.random.choice(['action', 'comedy', 'drama', 'sci-fi', 'animation'], 100)
        })
        
        # Gaming data
        self.demo_data['pokemon'] = pd.DataFrame({
            'pokemon_id': range(1, 101),
            'base_experience': np.random.exponential(100, 100).clip(50, 400),
            'attack': np.random.randint(20, 150, 100),
            'defense': np.random.randint(20, 150, 100),
            'speed': np.random.randint(20, 150, 100),
            'popularity_score': np.random.exponential(50, 100).clip(10, 100),
            'generation': np.random.choice([1, 2, 3, 4, 5], 100)
        })
        
        # Development data
        github_stars_base = 1000 + 50000 * np.random.exponential(0.1, 100)
        self.demo_data['repositories'] = pd.DataFrame({
            'repo_id': range(1, 101),
            'stars_count': github_stars_base,
            'forks_count': github_stars_base * np.random.uniform(0.1, 0.5, 100),
            'open_issues': np.random.poisson(50, 100),
            'language_score': np.random.uniform(0.1, 1.0, 100),
            'activity_score': np.random.exponential(0.3, 100).clip(0, 1),
            'created_year': np.random.choice(range(2010, 2024), 100)
        })
        
        # Time series data for temporal correlation
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        seasonal_pattern = np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
        
        self.demo_data['time_series'] = pd.DataFrame({
            'date': dates,
            'music_streams': 10000 + 5000 * seasonal_pattern + np.random.normal(0, 1000, len(dates)),
            'avg_temperature': 15 + 10 * seasonal_pattern + np.random.normal(0, 3, len(dates)),
            'movie_ticket_sales': 50000 + 20000 * seasonal_pattern + np.random.normal(0, 5000, len(dates)),
            'github_commits': 1000 + 200 * seasonal_pattern + np.random.normal(0, 100, len(dates))
        })
    
    def calculate_cross_domain_correlations(self) -> List[Dict[str, Any]]:
        """Calculate correlations between different data domains"""
        correlations = []
        
        # Weather-Music correlation
        weather_temp = self.demo_data['weather']['temperature']
        music_valence = self.demo_data['music']['valence']
        
        corr_coef, p_value = pearsonr(weather_temp, music_valence)
        correlations.append({
            'domain1': 'weather',
            'domain2': 'music',
            'variable1': 'temperature',
            'variable2': 'valence',
            'correlation_coefficient': corr_coef,
            'p_value': p_value,
            'method': 'pearson',
            'interpretation': self._interpret_correlation(corr_coef, p_value),
            'sample_size': len(weather_temp)
        })
        
        # Entertainment-Music correlation
        movie_revenue = self.demo_data['movies']['box_office_revenue']
        soundtrack_pop = self.demo_data['movies']['soundtrack_popularity']
        
        corr_coef, p_value = spearmanr(movie_revenue, soundtrack_pop)
        correlations.append({
            'domain1': 'entertainment',
            'domain2': 'music', 
            'variable1': 'box_office_revenue',
            'variable2': 'soundtrack_popularity',
            'correlation_coefficient': corr_coef,
            'p_value': p_value,
            'method': 'spearman',
            'interpretation': self._interpret_correlation(corr_coef, p_value),
            'sample_size': len(movie_revenue)
        })
        
        # Gaming-Music correlation
        pokemon_popularity = self.demo_data['pokemon']['popularity_score']
        music_energy = self.demo_data['music']['energy']
        
        corr_coef, p_value = pearsonr(pokemon_popularity, music_energy)
        correlations.append({
            'domain1': 'gaming',
            'domain2': 'music',
            'variable1': 'pokemon_popularity',
            'variable2': 'music_energy',
            'correlation_coefficient': corr_coef,
            'p_value': p_value,
            'method': 'pearson',
            'interpretation': self._interpret_correlation(corr_coef, p_value),
            'sample_size': len(pokemon_popularity)
        })
        
        return correlations
    
    def calculate_temporal_correlations(self) -> List[Dict[str, Any]]:
        """Calculate time-based correlations"""
        ts_data = self.demo_data['time_series']
        correlations = []
        
        # Music streams vs temperature over time
        corr_coef, p_value = pearsonr(ts_data['music_streams'], ts_data['avg_temperature'])
        correlations.append({
            'domain1': 'music',
            'domain2': 'weather',
            'variable1': 'daily_streams',
            'variable2': 'temperature',
            'correlation_coefficient': corr_coef,
            'p_value': p_value,
            'method': 'pearson_temporal',
            'interpretation': self._interpret_correlation(corr_coef, p_value),
            'sample_size': len(ts_data),
            'time_range': f"{ts_data['date'].min()} to {ts_data['date'].max()}"
        })
        
        # Movie sales vs GitHub activity
        corr_coef, p_value = pearsonr(ts_data['movie_ticket_sales'], ts_data['github_commits'])
        correlations.append({
            'domain1': 'entertainment',
            'domain2': 'development',
            'variable1': 'ticket_sales',
            'variable2': 'github_commits',
            'correlation_coefficient': corr_coef,
            'p_value': p_value,
            'method': 'pearson_temporal',
            'interpretation': self._interpret_correlation(corr_coef, p_value),
            'sample_size': len(ts_data),
            'time_range': f"{ts_data['date'].min()} to {ts_data['date'].max()}"
        })
        
        return correlations
    
    def _interpret_correlation(self, corr_coef: float, p_value: float) -> Dict[str, str]:
        """Interpret correlation strength and significance"""
        # Strength interpretation
        abs_corr = abs(corr_coef)
        if abs_corr >= 0.7:
            strength = "strong"
        elif abs_corr >= 0.3:
            strength = "moderate"
        elif abs_corr >= 0.1:
            strength = "weak"
        else:
            strength = "very_weak"
        
        # Direction
        direction = "positive" if corr_coef >= 0 else "negative"
        
        # Statistical significance
        significance = "significant" if p_value < 0.05 else "not_significant"
        
        return {
            "strength": strength,
            "direction": direction,
            "significance": significance,
            "business_relevance": self._assess_business_relevance(abs_corr, p_value < 0.05)
        }
    
    def _assess_business_relevance(self, abs_corr: float, is_significant: bool) -> str:
        """Assess business relevance of correlation"""
        if not is_significant:
            return "low"
        elif abs_corr >= 0.5:
            return "high"
        elif abs_corr >= 0.3:
            return "medium"
        else:
            return "low"
    
    def generate_correlation_heatmap(self, save_path: str = None):
        """Generate a correlation heatmap visualization"""
        # Create a combined correlation matrix
        combined_data = pd.DataFrame({
            'music_valence': self.demo_data['music']['valence'],
            'music_energy': self.demo_data['music']['energy'],
            'weather_temp': self.demo_data['weather']['temperature'],
            'weather_humidity': self.demo_data['weather']['humidity'],
            'movie_revenue': self.demo_data['movies']['box_office_revenue'],
            'soundtrack_pop': self.demo_data['movies']['soundtrack_popularity'],
            'pokemon_popularity': self.demo_data['pokemon']['popularity_score'],
            'github_stars': self.demo_data['repositories']['stars_count']
        })
        
        # Calculate correlation matrix
        correlation_matrix = combined_data.corr()
        
        # Create heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                    square=True, cbar_kws={'label': 'Correlation Coefficient'})
        plt.title('Cross-Domain Data Correlations\nData Centralization Platform Demo')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return correlation_matrix
    
    def run_entity_linking_demo(self) -> Dict[str, List[Dict]]:
        """Demonstrate entity linking across domains"""
        # Simulate ISRC code linking between music and movies
        linked_entities = {
            'music_movie_links': [
                {
                    'music_track_id': 1,
                    'movie_id': 1,
                    'link_type': 'soundtrack',
                    'isrc_code': 'GBAHS1500642',
                    'confidence': 0.95
                },
                {
                    'music_track_id': 25,
                    'movie_id': 33,
                    'link_type': 'featured_song',
                    'isrc_code': 'USRC17607839',
                    'confidence': 0.89
                }
            ],
            'geographic_links': [
                {
                    'weather_location': 'New York City',
                    'repository_location': 'New York, NY',
                    'coordinates': (40.7128, -74.0060),
                    'link_type': 'geographic_proximity',
                    'confidence': 1.0
                }
            ],
            'temporal_links': [
                {
                    'music_release_date': '2020-07-24',
                    'movie_release_date': '2020-12-25',
                    'link_type': 'same_year_release',
                    'temporal_distance_days': 154,
                    'confidence': 0.7
                }
            ]
        }
        
        return linked_entities
    
    def generate_summary_report(self) -> Dict[str, Any]:
        """Generate a comprehensive analysis report"""
        cross_correlations = self.calculate_cross_domain_correlations()
        temporal_correlations = self.calculate_temporal_correlations()
        entity_links = self.run_entity_linking_demo()
        
        # Calculate summary statistics
        significant_correlations = [
            corr for corr in cross_correlations + temporal_correlations 
            if corr['p_value'] < 0.05
        ]
        
        strong_correlations = [
            corr for corr in significant_correlations
            if abs(corr['correlation_coefficient']) >= 0.5
        ]
        
        summary = {
            'analysis_timestamp': datetime.now().isoformat(),
            'data_summary': {
                'total_domains': 5,
                'total_records': sum(len(df) for df in self.demo_data.values() if isinstance(df, pd.DataFrame)),
                'domains_analyzed': list(self.demo_data.keys())
            },
            'correlation_analysis': {
                'total_correlations_tested': len(cross_correlations) + len(temporal_correlations),
                'significant_correlations': len(significant_correlations),
                'strong_correlations': len(strong_correlations),
                'significant_rate': len(significant_correlations) / (len(cross_correlations) + len(temporal_correlations))
            },
            'top_correlations': sorted(
                significant_correlations,
                key=lambda x: abs(x['correlation_coefficient']),
                reverse=True
            )[:5],
            'entity_linking': {
                'total_links_found': sum(len(links) for links in entity_links.values()),
                'high_confidence_links': sum(
                    1 for links in entity_links.values()
                    for link in links if link['confidence'] >= 0.9
                ),
                'link_types': list(entity_links.keys())
            },
            'business_insights': self._generate_business_insights(significant_correlations)
        }
        
        return summary
    
    def _generate_business_insights(self, correlations: List[Dict]) -> List[str]:
        """Generate actionable business insights from correlations"""
        insights = []
        
        for corr in correlations:
            if corr['interpretation']['business_relevance'] == 'high':
                if corr['domain1'] == 'weather' and corr['domain2'] == 'music':
                    insights.append(
                        f"Weather patterns significantly influence music preferences. "
                        f"Playlist recommendations could be enhanced using real-time weather data."
                    )
                elif corr['domain1'] == 'entertainment' and corr['domain2'] == 'music':
                    insights.append(
                        f"Movie box office success correlates with soundtrack popularity. "
                        f"Music marketing strategies should align with film release schedules."
                    )
                elif 'temporal' in corr.get('method', ''):
                    insights.append(
                        f"Strong seasonal patterns detected between {corr['domain1']} and {corr['domain2']}. "
                        f"Consider seasonal marketing and content strategies."
                    )
        
        return insights


def main():
    """Run the correlation analysis demo"""
    print("🚀 Data Centralization Platform - Correlation Analysis Demo")
    print("=" * 60)
    
    # Initialize demo
    demo = CorrelationAnalysisDemo()
    
    # Run cross-domain correlations
    print("\\n📊 Calculating Cross-Domain Correlations...")
    cross_correlations = demo.calculate_cross_domain_correlations()
    
    for corr in cross_correlations:
        print(f"\\n{corr['domain1'].title()} ↔ {corr['domain2'].title()}")
        print(f"Variables: {corr['variable1']} vs {corr['variable2']}")
        print(f"Correlation: {corr['correlation_coefficient']:.3f} (p={corr['p_value']:.3f})")
        print(f"Strength: {corr['interpretation']['strength']} {corr['interpretation']['direction']}")
        print(f"Significance: {corr['interpretation']['significance']}")
        print(f"Business Relevance: {corr['interpretation']['business_relevance']}")
    
    # Run temporal correlations
    print("\\n⏰ Calculating Temporal Correlations...")
    temporal_correlations = demo.calculate_temporal_correlations()
    
    for corr in temporal_correlations:
        print(f"\\n{corr['domain1'].title()} ↔ {corr['domain2'].title()} (Time Series)")
        print(f"Variables: {corr['variable1']} vs {corr['variable2']}")
        print(f"Correlation: {corr['correlation_coefficient']:.3f} (p={corr['p_value']:.3f})")
        print(f"Time Range: {corr['time_range']}")
        print(f"Significance: {corr['interpretation']['significance']}")
    
    # Demonstrate entity linking
    print("\\n🔗 Entity Linking Demo...")
    entity_links = demo.run_entity_linking_demo()
    
    for link_type, links in entity_links.items():
        print(f"\\n{link_type.replace('_', ' ').title()}:")
        for link in links:
            print(f"  - {link}")
    
    # Generate comprehensive summary
    print("\\n📈 Generating Summary Report...")
    summary = demo.generate_summary_report()
    
    print(f"\\nAnalysis Summary:")
    print(f"  📁 Total domains analyzed: {summary['data_summary']['total_domains']}")
    print(f"  📊 Total records processed: {summary['data_summary']['total_records']}")
    print(f"  🔍 Correlations tested: {summary['correlation_analysis']['total_correlations_tested']}")
    print(f"  ✅ Significant correlations: {summary['correlation_analysis']['significant_correlations']}")
    print(f"  💪 Strong correlations: {summary['correlation_analysis']['strong_correlations']}")
    print(f"  📊 Significance rate: {summary['correlation_analysis']['significant_rate']:.1%}")
    
    print(f"\\n🎯 Business Insights:")
    for insight in summary['business_insights']:
        print(f"  • {insight}")
    
    # Generate correlation heatmap
    print("\\n📊 Generating Correlation Heatmap...")
    try:
        correlation_matrix = demo.generate_correlation_heatmap('correlation_heatmap.png')
        print("✅ Heatmap saved as 'correlation_heatmap.png'")
    except Exception as e:
        print(f"⚠️  Heatmap generation failed (display not available): {e}")
        correlation_matrix = demo.generate_correlation_heatmap()
    
    print("\\n🎉 Demo completed successfully!")
    print("\\nNext steps for full implementation:")
    print("  1. Set up PostgreSQL database with pgvector extension")
    print("  2. Run Alembic migrations to create schema")
    print("  3. Implement API clients authentication")
    print("  4. Build real-time data ingestion pipeline")
    print("  5. Develop LLM embedding generation for semantic search")
    print("  6. Create interactive dashboard with real-time correlations")


if __name__ == "__main__":
    # Run the demonstration
    main()
