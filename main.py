# CS 363 Project: Geopolitical Alliances and Strategic Deterrence Analysis of the Israel-Palestine Conflict
# Author: Syeda Hoorain Imran
import os
from clean_data import load_and_clean_data
from build_graphs import build_bipartite_graph, project_alliance_network, project_issue_network
from calculate_metrics import extract_backbones, calculate_alliance_metrics, calculate_issue_metrics
import networkx as nx

def export_graphs(B, G_alliance, G_issue, filtered_countries, filtered_resolutions):
    # Export all graph stages
    print("Exporting graphs")

    nx.write_graphml(B, '01_base_bipartite_network.graphml')
    nx.write_graphml(G_alliance, '02_countries_network.graphml')
    nx.write_graphml(G_issue, '03_resolutions_network.graphml')
    nx.write_graphml(filtered_countries, '04_filtered_countries.graphml')
    nx.write_graphml(filtered_resolutions, '05_filtered_resolutions.graphml')

    print("Exported 5 GraphML files")

def generate_report(filtered_countries, filtered_resolutions, betweenness, eigenvector, partition, modularity_score, degree_centrality):
    # Print simple results summary
    print("\nCS363 Project - Run Complete. Results Summary:")

    # Network stats
    alliance_density = nx.density(filtered_countries)
    issue_density = nx.density(filtered_resolutions)

    print(f"Filtered Countries Network: {len(filtered_countries.nodes())} nodes, {len(filtered_countries.edges())} edges")
    print(f"Density: {alliance_density:.4f}")
    print(f"Filtered Resolutions Network: {len(filtered_resolutions.nodes())} nodes, {len(filtered_resolutions.edges())} edges")
    print(f"Density: {issue_density:.4f}")

    # Communities
    num_communities = len(set(partition.values()))
    print(f"Communities: {num_communities}")
    print(f"Modularity: {modularity_score:.4f}")

    # Pakistan analysis
    print("\nPakistan Analysis:")
    if 'PAKISTAN' in filtered_countries.nodes():
        pak_betweenness = betweenness.get('PAKISTAN', 0)
        pak_eigenvector = eigenvector.get('PAKISTAN', 0)
        pak_community = partition.get('PAKISTAN', 'N/A')

        print(f"Betweenness: {pak_betweenness:.6f}")
        print(f"Eigenvector: {pak_eigenvector:.4f}")
        print(f"Community: {pak_community}")

        # Top allies
        allies = [(neighbor, filtered_countries['PAKISTAN'][neighbor]['weight'])
                 for neighbor in filtered_countries.neighbors('PAKISTAN')]
        allies.sort(key=lambda x: x[1], reverse=True)

        print("Top 5 Allies:")
        for i, (ally, weight) in enumerate(allies[:5], 1):
            print(f"  {i}. {ally}: {weight:.3f}")
    else:
        print("Pakistan not in filtered network.")

    # Issue correlations
    print("\nTop Resolution Pairs:")
    if filtered_resolutions.edges():
        edge_weights = [(u, v, data['weight']) for u, v, data in filtered_resolutions.edges(data=True)]
        edge_weights.sort(key=lambda x: x[2], reverse=True)

        for i, (res1, res2, weight) in enumerate(edge_weights[:3], 1):
            print(f"  {i}. {res1} ↔ {res2}: {weight:.3f}")
    else:
        print("No edges in filtered resolutions.")

def main():
    # Main pipeline
    print("UN Voting Analysis - Israel-Palestine")

    # Data
    df_bipartite, total_resolutions = load_and_clean_data()

    # Graphs
    B = build_bipartite_graph(df_bipartite)
    G_alliance = project_alliance_network(B, total_resolutions)
    G_issue = project_issue_network(B, total_resolutions)

    # Filter
    filtered_countries, filtered_resolutions = extract_backbones(G_alliance, G_issue)

    # Metrics
    betweenness, eigenvector, partition, modularity_score = calculate_alliance_metrics(filtered_countries)
    degree_centrality = calculate_issue_metrics(filtered_resolutions)

    # Export
    export_graphs(B, G_alliance, G_issue, filtered_countries, filtered_resolutions)

    # Report
    generate_report(filtered_countries, filtered_resolutions, betweenness, eigenvector, partition, modularity_score, degree_centrality)

    print("\nDone. Check the 5 .graphml files.")

if __name__ == "__main__":
    main()


