"""
Network Graph Visualization

Creates interactive network graphs showing relationships between entities
across different domains using NetworkX and Plotly.
"""

import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Dict, Any, Tuple
import numpy as np
import math


class NetworkVisualizer:
    """
    Service for creating network visualizations of entity relationships
    """
    
    def __init__(self):
        self.color_map = {
            'music': '#1f77b4',      # Blue
            'weather': '#ff7f0e',    # Orange  
            'entertainment': '#2ca02c', # Green
            'gaming': '#d62728',     # Red
            'development': '#9467bd', # Purple
            'productivity': '#8c564b'  # Brown
        }
    
    def create_correlation_network(self, 
                                 correlations: List[Dict[str, Any]], 
                                 threshold: float = 0.3,
                                 title: str = "Cross-Domain Correlation Network") -> go.Figure:
        """
        Create a network graph showing correlations as connections between domains
        
        Args:
            correlations: List of correlation dictionaries
            threshold: Minimum correlation strength to include
            title: Graph title
            
        Returns:
            Plotly Figure object
        """
        # Create NetworkX graph
        G = nx.Graph()
        
        # Add nodes and edges based on correlations
        for corr in correlations:
            if abs(corr['correlation_coefficient']) >= threshold and corr.get('p_value', 1) < 0.05:
                
                domain1 = corr['domain1']
                domain2 = corr['domain2']
                strength = abs(corr['correlation_coefficient'])
                
                # Add nodes
                G.add_node(domain1, domain=domain1)
                G.add_node(domain2, domain=domain2)
                
                # Add edge with correlation strength as weight
                G.add_edge(domain1, domain2, 
                          weight=strength,
                          correlation=corr['correlation_coefficient'],
                          p_value=corr.get('p_value', 0),
                          variables=f"{corr['variable1']} ↔ {corr['variable2']}")
        
        if len(G.nodes()) == 0:
            # Return empty figure if no correlations meet threshold
            fig = go.Figure()
            fig.add_annotation(text="No correlations meet the threshold criteria", 
                             xref="paper", yref="paper", x=0.5, y=0.5,
                             showarrow=False, font_size=16)
            return fig
        
        # Generate layout
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        # Extract node and edge information
        node_trace, edge_trace = self._create_network_traces(G, pos)
        
        # Create figure
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title=dict(text=title, font=dict(size=16)),
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           annotations=[ dict(
                               text="Node size represents connectivity, edge thickness represents correlation strength",
                               showarrow=False,
                               xref="paper", yref="paper",
                               x=0.005, y=-0.002,
                               xanchor="left", yanchor="bottom",
                               font=dict(size=12)
                           )],
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           width=800,
                           height=600
                       ))
        
        return fig
    
    def create_entity_relationship_network(self, 
                                         entity_links: Dict[str, List[Dict]], 
                                         title: str = "Entity Relationship Network") -> go.Figure:
        """
        Create a network graph showing relationships between individual entities
        
        Args:
            entity_links: Dictionary of entity relationship data
            title: Graph title
            
        Returns:
            Plotly Figure object
        """
        G = nx.Graph()
        
        # Add nodes and edges from entity links
        for link_type, links in entity_links.items():
            for link in links:
                if link_type == 'music_movie_links':
                    # Music-Movie connections
                    music_node = f"Track_{link['music_track_id']}"
                    movie_node = f"Movie_{link['movie_id']}"
                    
                    G.add_node(music_node, domain='music', type='track')
                    G.add_node(movie_node, domain='entertainment', type='movie')
                    G.add_edge(music_node, movie_node, 
                              relationship=link['link_type'],
                              confidence=link['confidence'],
                              isrc=link.get('isrc_code', ''))
                
                elif link_type == 'geographic_links':
                    # Geographic connections
                    weather_node = f"Weather_{link['weather_location']}"
                    repo_node = f"Repo_{link['repository_location']}"
                    
                    G.add_node(weather_node, domain='weather', type='location')
                    G.add_node(repo_node, domain='development', type='location')
                    G.add_edge(weather_node, repo_node,
                              relationship=link['link_type'],
                              confidence=link['confidence'])
        
        if len(G.nodes()) == 0:
            fig = go.Figure()
            fig.add_annotation(text="No entity relationships to display", 
                             xref="paper", yref="paper", x=0.5, y=0.5,
                             showarrow=False, font_size=16)
            return fig
        
        # Generate layout
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Create traces
        edge_trace, node_traces = self._create_entity_network_traces(G, pos)
        
        # Combine all traces
        all_traces = [edge_trace] + node_traces
        
        # Create figure
        fig = go.Figure(data=all_traces,
                       layout=go.Layout(
                           title=dict(text=title, font=dict(size=16)),
                           showlegend=True,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           width=800,
                           height=600
                       ))
        
        return fig
    
    def _create_network_traces(self, G: nx.Graph, pos: Dict) -> Tuple[go.Scatter, go.Scatter]:
        """Create node and edge traces for domain correlation network"""
        
        # Edge trace
        edge_x = []
        edge_y = []
        edge_info = []
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            
            # Edge hover info
            edge_data = G.edges[edge]
            edge_info.append(f"{edge[0]} ↔ {edge[1]}<br>"
                           f"Correlation: {edge_data['correlation']:.3f}<br>"
                           f"Variables: {edge_data['variables']}<br>"
                           f"P-value: {edge_data['p_value']:.3f}")
        
        edge_trace = go.Scatter(x=edge_x, y=edge_y,
                               line=dict(width=2, color='#888'),
                               hoverinfo='none',
                               mode='lines')
        
        # Node trace
        node_x = []
        node_y = []
        node_info = []
        node_colors = []
        node_sizes = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            # Node size based on degree (connectivity)
            degree = G.degree(node)
            node_sizes.append(20 + degree * 10)
            
            # Node color based on domain
            node_colors.append(self.color_map.get(node, '#888'))
            
            # Node hover info
            connections = list(G.neighbors(node))
            node_info.append(f"Domain: {node}<br>"
                           f"Connections: {len(connections)}<br>"
                           f"Connected to: {', '.join(connections)}")
        
        node_trace = go.Scatter(x=node_x, y=node_y,
                               mode='markers+text',
                               hoverinfo='text',
                               text=list(G.nodes()),
                               textposition="middle center",
                               hovertext=node_info,
                               marker=dict(size=node_sizes,
                                         color=node_colors,
                                         line=dict(width=2, color='white')))
        
        return node_trace, edge_trace
    
    def _create_entity_network_traces(self, G: nx.Graph, pos: Dict) -> Tuple[go.Scatter, go.Scatter]:
        """Create node and edge traces for entity relationship network"""
        
        # Edge trace
        edge_x = []
        edge_y = []
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        edge_trace = go.Scatter(x=edge_x, y=edge_y,
                               line=dict(width=1, color='#888'),
                               hoverinfo='none',
                               mode='lines')
        
        # Node traces (separate by domain for legend)
        traces = [edge_trace]
        
        for domain in set(G.nodes[node].get('domain', 'unknown') for node in G.nodes()):
            domain_nodes = [node for node in G.nodes() if G.nodes[node].get('domain') == domain]
            
            if not domain_nodes:
                continue
                
            node_x = [pos[node][0] for node in domain_nodes]
            node_y = [pos[node][1] for node in domain_nodes]
            node_text = [node.split('_')[1] if '_' in node else node for node in domain_nodes]
            
            node_info = []
            for node in domain_nodes:
                node_data = G.nodes[node]
                connections = list(G.neighbors(node))
                node_info.append(f"Entity: {node}<br>"
                               f"Domain: {domain}<br>"
                               f"Type: {node_data.get('type', 'unknown')}<br>"
                               f"Connections: {len(connections)}")
            
            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                name=domain.title(),
                text=node_text,
                textposition="middle center",
                hoverinfo='text',
                hovertext=node_info,
                marker=dict(
                    size=15,
                    color=self.color_map.get(domain, '#888'),
                    line=dict(width=1, color='white')
                )
            )
            
            traces.append(node_trace)
        
        return traces[0], traces[1:]  # Return edge_trace and list of node traces
    
    def create_temporal_correlation_graph(self, 
                                        time_series_data: pd.DataFrame,
                                        variables: List[str],
                                        title: str = "Temporal Correlation Patterns") -> go.Figure:
        """
        Create a time series graph showing multiple variables over time
        
        Args:
            time_series_data: DataFrame with time series data
            variables: List of variable names to plot
            title: Graph title
            
        Returns:
            Plotly Figure object
        """
        fig = go.Figure()
        
        # Color palette for different variables
        colors = px.colors.qualitative.Set1
        
        for i, var in enumerate(variables):
            if var in time_series_data.columns:
                fig.add_trace(go.Scatter(
                    x=time_series_data.index,
                    y=time_series_data[var],
                    mode='lines',
                    name=var.replace('_', ' ').title(),
                    line=dict(color=colors[i % len(colors)])
                ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Time",
            yaxis_title="Value",
            hovermode='x unified',
            width=800,
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig


# Demo function
def create_demo_network():
    """Create a demo network visualization"""
    
    # Sample correlation data
    demo_correlations = [
        {
            'domain1': 'music',
            'domain2': 'weather',
            'variable1': 'valence',
            'variable2': 'temperature',
            'correlation_coefficient': 0.65,
            'p_value': 0.001
        },
        {
            'domain1': 'entertainment',
            'domain2': 'music',
            'variable1': 'box_office',
            'variable2': 'soundtrack_popularity',
            'correlation_coefficient': 0.78,
            'p_value': 0.0001
        },
        {
            'domain1': 'weather',
            'domain2': 'gaming',
            'variable1': 'precipitation',
            'variable2': 'indoor_activity',
            'correlation_coefficient': 0.45,
            'p_value': 0.01
        }
    ]
    
    # Sample entity links
    demo_entity_links = {
        'music_movie_links': [
            {
                'music_track_id': 1,
                'movie_id': 101,
                'link_type': 'soundtrack',
                'confidence': 0.95,
                'isrc_code': 'GBAHS1500642'
            }
        ],
        'geographic_links': [
            {
                'weather_location': 'New York City',
                'repository_location': 'New York, NY',
                'link_type': 'geographic_proximity',
                'confidence': 1.0
            }
        ]
    }
    
    visualizer = NetworkVisualizer()
    
    # Create correlation network
    correlation_fig = visualizer.create_correlation_network(demo_correlations)
    correlation_fig.write_html("correlation_network.html")
    
    # Create entity relationship network
    entity_fig = visualizer.create_entity_relationship_network(demo_entity_links)
    entity_fig.write_html("entity_network.html")
    
    print("Demo network visualizations created:")
    print("- correlation_network.html")
    print("- entity_network.html")


if __name__ == "__main__":
    create_demo_network()
