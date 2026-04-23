# CS 363 Project: Geopolitical Alliances and Strategic Deterrence Analysis of the Israel-Palestine Conflict
# Author: Syeda Hoorain Imran

import networkx as nx
import community

def extract_backbones(G_alliance, G_issue):
    # Apply thresholding to extract backbones
    print("Extracting backbones...")

    # Alliance backbone: weight >= 0.70
    alliance_backbone = nx.Graph()
    for u, v, data in G_alliance.edges(data=True):
        if data['weight'] >= 0.70:
            alliance_backbone.add_edge(u, v, weight=data['weight'])

    # Issue backbone: weight >= 0.80
    issue_backbone = nx.Graph()
    for u, v, data in G_issue.edges(data=True):
        if data['weight'] >= 0.80:
            issue_backbone.add_edge(u, v, weight=data['weight'])

    print(f"Alliance backbone: {len(alliance_backbone.nodes())} nodes, {len(alliance_backbone.edges())} edges")
    print(f"Issue backbone: {len(issue_backbone.nodes())} nodes, {len(issue_backbone.edges())} edges")

    return alliance_backbone, issue_backbone

def calculate_alliance_metrics(G_alliance):
    # Calculate advanced metrics for alliance network
    print("Calculating Alliance Network metrics...")

    # Betweenness Centrality (Brokers)
    betweenness = nx.betweenness_centrality(G_alliance, weight='weight', normalized=True)

    # Eigenvector Centrality (Influence)
    eigenvector = nx.eigenvector_centrality(G_alliance, weight='weight', max_iter=1000)

    # Community Detection (Louvain)
    partition = community.best_partition(G_alliance, weight='weight')
    modularity_score = community.modularity(partition, G_alliance, weight='weight')

    # Add attributes to graph
    nx.set_node_attributes(G_alliance, betweenness, 'betweenness')
    nx.set_node_attributes(G_alliance, eigenvector, 'eigenvector')
    nx.set_node_attributes(G_alliance, partition, 'community')

    print(f"Communities detected: {len(set(partition.values()))}")
    print(f"Modularity score: {modularity_score:.4f}")

    return betweenness, eigenvector, partition, modularity_score

def calculate_issue_metrics(G_issue):
    # Calculate metrics for issue network
    print("Calculating Issue Network metrics...")

    # Degree Centrality (most linked resolutions)
    degree_centrality = nx.degree_centrality(G_issue)

    # Add to graph
    nx.set_node_attributes(G_issue, degree_centrality, 'degree_centrality')

    return degree_centrality