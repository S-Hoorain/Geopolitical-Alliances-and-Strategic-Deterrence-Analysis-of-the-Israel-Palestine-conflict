# CS 363 Project: Geopolitical Alliances and Strategic Deterrence Analysis of the Israel-Palestine Conflict
# Author: Syeda Hoorain Imran

import networkx as nx
import itertools

def build_bipartite_graph(df):
    # Build the bipartite graph from voting data
    print("Building bipartite graph...")

    B = nx.Graph()

    countries = df['Country'].unique()
    resolutions = df['Resolution_ID'].unique()

    # Add nodes
    for country in countries:
        B.add_node(country, bipartite=0)
    for resolution in resolutions:
        B.add_node(resolution, bipartite=1)

    # Add edges
    for _, row in df.iterrows():
        country = row['Country']
        resolution = row['Resolution_ID']
        vote = row['Vote_Value']
        B.add_edge(country, resolution, weight=vote)

    print(f"Bipartite graph: {len(B.nodes())} nodes, {len(B.edges())} edges")
    return B

def project_alliance_network(B, total_resolutions):
    # Project onto countries to get alliance network
    print("Projecting Alliance Network (Countries)...")

    countries = [node for node, attr in B.nodes(data=True) if attr['bipartite'] == 0]
    G_alliance = nx.Graph()

    for country1, country2 in itertools.combinations(countries, 2):
        shared_resolutions = set(B.neighbors(country1)) & set(B.neighbors(country2))

        if shared_resolutions:
            agreement_score = 0
            for resolution in shared_resolutions:
                vote1 = B[country1][resolution]['weight']
                vote2 = B[country2][resolution]['weight']
                if vote1 == vote2:
                    agreement_score += 1
                else:
                    agreement_score -= 1

            normalized_weight = agreement_score / total_resolutions
            G_alliance.add_edge(country1, country2, weight=normalized_weight)

    print(f"Alliance network: {len(G_alliance.nodes())} nodes, {len(G_alliance.edges())} edges")
    return G_alliance

def project_issue_network(B, total_resolutions):
    # Project onto resolutions to get issue network
    print("Projecting Issue Network (Resolutions)...")

    resolutions = [node for node, attr in B.nodes(data=True) if attr['bipartite'] == 1]
    G_issue = nx.Graph()

    for res1, res2 in itertools.combinations(resolutions, 2):
        shared_countries = set(B.neighbors(res1)) & set(B.neighbors(res2))

        if shared_countries:
            agreement_score = 0
            for country in shared_countries:
                vote1 = B[res1][country]['weight']
                vote2 = B[res2][country]['weight']
                if vote1 == vote2:
                    agreement_score += 1
                else:
                    agreement_score -= 1

            normalized_weight = agreement_score / total_resolutions
            G_issue.add_edge(res1, res2, weight=normalized_weight)

    print(f"Issue network: {len(G_issue.nodes())} nodes, {len(G_issue.edges())} edges")
    return G_issue