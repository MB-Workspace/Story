"""
Graph Processing Module with NetworkX Integration
"""
import networkx as nx
from typing import Dict, Any, List, Tuple

class GraphProcessor:
    """Process entity graphs using NetworkX algorithms"""
    
    def __init__(self, entity_graph: Dict[str, Dict[str, Any]]) -> None:
        """Initialize with entity graph from EvidenceCorrelator"""
        self.entity_graph = entity_graph
        self.nx_graph = self._convert_to_nx_graph()
    
    def _convert_to_nx_graph(self) -> nx.Graph:
        """Convert entity graph dictionary to NetworkX graph"""
        G = nx.Graph()
        
        # Add nodes with metadata
        for node, data in self.entity_graph.items():
            G.add_node(node, **data["metadata"])
            
        # Add edges
        for node, data in self.entity_graph.items():
            for neighbor in data["connections"]:
                if neighbor in self.entity_graph:
                    G.add_edge(node, neighbor)
                    
        return G
    
    def detect_shell_networks(self, min_component_size: int = 3) -> List[List[str]]:
        """Detect multi-hop shell networks using BFS traversal
        
        Args:
            min_component_size: Minimum number of nodes to flag as shell network
        """
        shell_networks = []
        visited = set()
        
        for node in self.nx_graph.nodes():
            if node in visited:
                continue
                
            # Find connected components
            component = list(nx.node_connected_component(self.nx_graph, node))
            visited.update(component)
            
            # Only consider components with at least min_component_size nodes
            if len(component) >= min_component_size:
                shell_networks.append(component)
                
        return shell_networks
    
    def calculate_centralities(self) -> Dict[str, Dict[str, float]]:
        """Calculate various centrality metrics for all nodes"""
        centralities = {
            "degree": nx.degree_centrality(self.nx_graph),
            "betweenness": nx.betweenness_centrality(self.nx_graph),
            "eigenvector": nx.eigenvector_centrality(self.nx_graph, max_iter=1000),
            "closeness": nx.closeness_centrality(self.nx_graph)
        }
        
        # Format results
        result = {}
        for node in self.nx_graph.nodes():
            result[node] = {
                metric: values[node] 
                for metric, values in centralities.items()
            }
            
        return result
    
    def find_key_nodes(self, top_n: int = 5) -> List[Tuple[str, float]]:
        """Identify top N most central nodes"""
        betweenness = nx.betweenness_centrality(self.nx_graph)
        sorted_nodes = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)
        return sorted_nodes[:top_n]
    
    def detect_rings(self, ring_size: int = 3) -> List[List[str]]:
        """Detect ring structures of given size"""
        rings = []
        
        # Find all cycles
        for cycle in nx.simple_cycles(self.nx_graph.to_directed()):
            if len(cycle) == ring_size:
                rings.append(cycle)
                
        return rings