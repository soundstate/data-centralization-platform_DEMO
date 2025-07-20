"""
Correlation Visualization Service

Generates interactive heatmaps and network visualizations
for the data centralization platform, using Plotly for interactivity.
"""

import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any


class CorrelationVisualizer:
    """
    Visualization service for creating interactive plots of correlation data
    """
    
    def create_interactive_heatmap(self, 
                                   correlation_matrix: pd.DataFrame,
                                   title: str = "Cross-Domain Correlation Heatmap") -> go.Figure:
        """
        Create an interactive heatmap visualization for correlation data
        
        Args:
            correlation_matrix: Pandas DataFrame of correlations
            title: Title of the heatmap figure
            
        Returns:
            A Plotly Figure object representing the heatmap
        """
        # Prepare heatmap
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.index,
            colorscale='Viridis',
            colorbar=dict(title='Correlation Coefficient'),
            zmid=0  # Midpoint for divergent color scale
        ))
        
        # Add metadata and layout
        fig.update_layout(
            title=title,
            xaxis_nticks=len(correlation_matrix.columns),
            yaxis_nticks=len(correlation_matrix.index),
            hovermode="closest",
            template="plotly_dark"
        )
        
        return fig


# Utility function for demonstration
if __name__ == "__main__":
    # Generate a sample correlation matrix
    sample_matrix = pd.DataFrame(
        [
            [1.0, 0.5, -0.3],
            [0.5, 1.0, 0.4],
            [-0.3, 0.4, 1.0]
        ],
        columns=["Music", "Weather", "Entertainment"],
        index=["Music", "Weather", "Entertainment"]
    )
    
    # Visualize
    visualizer = CorrelationVisualizer()
    heatmap_fig = visualizer.create_interactive_heatmap(sample_matrix)
    
    # Output to HTML file
    heatmap_fig.write_html("correlation_heatmap.html")
    print("Interactive heatmap generated: 'correlation_heatmap.html'")

