"""
Visualization Demo Script

Tests the interactive visualization components including correlation heatmaps,
network graphs, and dashboard functionality.
"""

import sys
import os
import asyncio

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.correlation_analysis_demo import CorrelationAnalysisDemo
from packages.shared_core.shared_core.visualization.correlation_visualizer import CorrelationVisualizer
from packages.shared_core.shared_core.visualization.network_visualizer import NetworkVisualizer
import pandas as pd


def test_correlation_heatmap():
    """Test the correlation heatmap visualization"""
    print("🎨 Testing Correlation Heatmap...")
    
    # Load demo data
    demo = CorrelationAnalysisDemo()
    
    # Create combined correlation matrix
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
    
    # Create visualization
    visualizer = CorrelationVisualizer()
    fig = visualizer.create_interactive_heatmap(
        correlation_matrix, 
        title="Data Centralization Platform - Cross-Domain Correlations"
    )
    
    # Save as HTML
    output_file = "interactive_correlation_heatmap.html"
    fig.write_html(output_file)
    print(f"✅ Correlation heatmap saved to: {output_file}")
    
    return fig


def test_network_visualization():
    """Test the network graph visualization"""
    print("🕸️ Testing Network Graph Visualization...")
    
    # Load demo data
    demo = CorrelationAnalysisDemo()
    cross_correlations = demo.calculate_cross_domain_correlations()
    temporal_correlations = demo.calculate_temporal_correlations()
    entity_links = demo.run_entity_linking_demo()
    
    # Create network visualizer
    network_viz = NetworkVisualizer()
    
    # Create correlation network
    correlation_fig = network_viz.create_correlation_network(
        cross_correlations + temporal_correlations,
        threshold=0.3,
        title="Cross-Domain Correlation Network"
    )
    
    correlation_output = "correlation_network_demo.html"
    correlation_fig.write_html(correlation_output)
    print(f"✅ Correlation network saved to: {correlation_output}")
    
    # Create entity relationship network
    entity_fig = network_viz.create_entity_relationship_network(
        entity_links,
        title="Entity Relationship Network"
    )
    
    entity_output = "entity_network_demo.html"
    entity_fig.write_html(entity_output)
    print(f"✅ Entity network saved to: {entity_output}")
    
    # Create temporal correlation graph
    temporal_fig = network_viz.create_temporal_correlation_graph(
        demo.demo_data['time_series'],
        ['music_streams', 'avg_temperature', 'movie_ticket_sales', 'github_commits'],
        title="Temporal Correlation Patterns"
    )
    
    temporal_output = "temporal_correlations.html"
    temporal_fig.write_html(temporal_output)
    print(f"✅ Temporal correlations saved to: {temporal_output}")
    
    return correlation_fig, entity_fig, temporal_fig


def test_dashboard_data():
    """Test dashboard data loading and processing"""
    print("📊 Testing Dashboard Data Loading...")
    
    # Load demo data
    demo = CorrelationAnalysisDemo()
    
    # Test correlation calculations
    cross_correlations = demo.calculate_cross_domain_correlations()
    temporal_correlations = demo.calculate_temporal_correlations()
    entity_links = demo.run_entity_linking_demo()
    summary = demo.generate_summary_report()
    
    print(f"✅ Data loading successful:")
    print(f"   - Cross-domain correlations: {len(cross_correlations)}")
    print(f"   - Temporal correlations: {len(temporal_correlations)}")
    print(f"   - Entity links: {sum(len(links) for links in entity_links.values())}")
    print(f"   - Total records: {summary['data_summary']['total_records']}")
    print(f"   - Significant correlations: {summary['correlation_analysis']['significant_correlations']}")
    
    return summary


def generate_demo_report():
    """Generate a comprehensive demo report"""
    print("📝 Generating Demo Report...")
    
    demo = CorrelationAnalysisDemo()
    summary = demo.generate_summary_report()
    
    # Create report
    report = f"""
# Data Centralization Platform - Demo Report
Generated: {summary['analysis_timestamp']}

## Overview
- **Total Domains**: {summary['data_summary']['total_domains']}
- **Total Records**: {summary['data_summary']['total_records']}
- **Domains Analyzed**: {', '.join(summary['data_summary']['domains_analyzed'])}

## Correlation Analysis Results
- **Correlations Tested**: {summary['correlation_analysis']['total_correlations_tested']}
- **Significant Correlations**: {summary['correlation_analysis']['significant_correlations']}
- **Strong Correlations**: {summary['correlation_analysis']['strong_correlations']}
- **Significance Rate**: {summary['correlation_analysis']['significant_rate']:.1%}

## Top Correlations
"""
    
    for i, corr in enumerate(summary['top_correlations'][:3], 1):
        report += f"""
### {i}. {corr['domain1'].title()} ↔ {corr['domain2'].title()}
- **Variables**: {corr['variable1']} vs {corr['variable2']}
- **Correlation**: {corr['correlation_coefficient']:.3f}
- **P-value**: {corr['p_value']:.3f}
- **Method**: {corr['method']}
- **Sample Size**: {corr['sample_size']}
"""
    
    report += f"""
## Entity Linking
- **Total Links Found**: {summary['entity_linking']['total_links_found']}
- **High Confidence Links**: {summary['entity_linking']['high_confidence_links']}
- **Link Types**: {', '.join(summary['entity_linking']['link_types'])}

## Business Insights
"""
    
    for insight in summary['business_insights']:
        report += f"- {insight}\n"
    
    report += f"""
## Generated Visualizations
- `interactive_correlation_heatmap.html` - Interactive correlation matrix
- `correlation_network_demo.html` - Cross-domain correlation network
- `entity_network_demo.html` - Entity relationship network  
- `temporal_correlations.html` - Time series correlation patterns

## Next Steps
1. Set up PostgreSQL database with pgvector extension
2. Configure OpenAI API key for semantic search
3. Run Streamlit dashboard: `streamlit run dashboard/streamlit_dashboard.py`
4. Implement live API data collection
5. Deploy production environment

---
*Data Centralization Platform - Proof of Concept*
"""
    
    # Save report
    with open("demo_report.md", "w") as f:
        f.write(report)
    
    print("✅ Demo report saved to: demo_report.md")
    return report


def main():
    """Run the complete visualization demo"""
    print("🚀 Data Centralization Platform - Visualization Demo")
    print("=" * 60)
    
    try:
        # Test correlation heatmap
        heatmap_fig = test_correlation_heatmap()
        print()
        
        # Test network visualizations
        correlation_net, entity_net, temporal_fig = test_network_visualization()
        print()
        
        # Test dashboard data
        summary = test_dashboard_data()
        print()
        
        # Generate demo report
        report = generate_demo_report()
        print()
        
        print("🎉 All visualization tests completed successfully!")
        print()
        print("📁 Generated Files:")
        print("   - interactive_correlation_heatmap.html")
        print("   - correlation_network_demo.html")
        print("   - entity_network_demo.html")
        print("   - temporal_correlations.html")
        print("   - demo_report.md")
        print()
        print("🖥️  To run the interactive dashboard:")
        print("   streamlit run dashboard/streamlit_dashboard.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during visualization demo: {e}")
        return False


if __name__ == "__main__":
    success = main()
