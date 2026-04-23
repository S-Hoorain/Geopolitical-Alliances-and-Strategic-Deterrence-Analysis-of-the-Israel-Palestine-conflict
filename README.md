# Geopolitical Alliances and Strategic Deterrence: SNA of the Israel-Palestine Conflict

## Overview

This is a CS 363 Network Games project that analyzes UN General Assembly voting patterns on Israel-Palestine related resolutions from October 7, 2023, onward. Using social network analysis, the project constructs diplomatic alliance networks and identifies geopolitical blocs, with a detailed focus on Pakistan's structural positioning within the global voting coalitions.

## The Pipeline

### Python Modules

- **`clean_data.py`** — Loads UN voting records from `outcomes.csv` and `voting.csv`. Filters for Israel-Palestine resolutions post-October 7, 2023, standardizes country names, maps vote values (Yes=1, No=-1, Abstain=0), and returns the cleaned bipartite data.

- **`build_graphs.py`** — Constructs the bipartite graph (countries × resolutions) and performs dual weighted projections. The alliance network connects countries by voting agreement; the issue network connects resolutions by voting similarity.

- **`calculate_metrics.py`** — Extracts backbone networks using thresholding (countries ≥ 0.70, resolutions ≥ 0.80). Calculates centrality metrics (betweenness, eigenvector) and performs community detection using the Louvain algorithm.

- **`main.py`** — Orchestrates the entire pipeline. Cleans up old files, imports all modules, executes each stage, exports all graph stages, and generates a terminal summary with Pakistan analysis.

### Generated GraphML Files

The pipeline exports 5 GraphML files showing the progression from raw data to refined networks:

1. **`01_base_bipartite.graphml`** — The raw bipartite graph with all 235 nodes (191 countries + 44 resolutions) and 6,714 edges.

2. **`02_full_countries.graphml`** — Full country alliance network (191 countries, 18,127 edges) before thresholding.

3. **`03_full_resolutions.graphml`** — Full resolution network (44 resolutions, 946 edges) before thresholding.

4. **`04_filtered_countries.graphml`** — Backbone country network with weight ≥ 0.70 (138 countries, 7,912 edges). Represents strongest diplomatic alliances.

5. **`05_filtered_resolutions.graphml`** — Backbone resolution network with weight ≥ 0.80 (44 nodes, 946 edges). Shows highly correlated voting patterns.

All files include node attributes for centrality, community membership, and other metrics for visualization in Gephi.

## Installation & Usage

### Requirements

```
pandas
networkx
python-louvain
```

Install via pip:
```bash
pip install pandas networkx python-louvain
```

### Running the Analysis

Execute the entire pipeline:
```bash
python main.py
```

The script will:
- Load and clean UN voting data
- Build bipartite and projected networks
- Extract backbones and calculate metrics
- Export all 5 GraphML files
- Print a summary with network statistics and Pakistan analysis

## Data

The project requires two CSV files that are too large for GitHub (347 MB total). Download them from the UN data source or contact the author for access:

- `outcomes.csv`: UN resolution metadata
- `voting.csv`: Individual country votes

Place these files in the same directory as `main.py` before running the analysis.

## Output

The terminal output includes:
- Network statistics (node count, edge count, density)
- Community detection results (number of blocs, modularity score)
- Pakistan's centrality metrics (betweenness, eigenvector)
- Top 5 diplomatic allies for Pakistan
- Structurally correlated resolution pairs

All GraphML files are ready for visualization in Gephi or other network analysis tools.

## Author

Syeda Hoorain Imran — CS 363 Network Games