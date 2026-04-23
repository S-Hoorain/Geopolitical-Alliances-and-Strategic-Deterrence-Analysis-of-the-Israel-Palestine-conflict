# CS 363 Project: Geopolitical Alliances and Strategic Deterrence Analysis of the Israel-Palestine Conflict
# Author: Syeda Hoorain Imran

import pandas as pd

def load_and_clean_data(filepath='outcomes.csv', voting_filepath='voting.csv'):
    # Load and clean UN voting data for Israel-Palestine resolutions
    print("Loading and processing source data...")

    # Load outcomes.csv
    outcomes_df = pd.read_csv(filepath)
    outcomes_df['date'] = pd.to_datetime(outcomes_df['date'])

    # Filter for post-October 7, 2023
    cutoff_date = pd.to_datetime('2023-10-07')
    outcomes_filtered = outcomes_df[outcomes_df['date'] >= cutoff_date].copy()

    # Filter for Israel-Palestine related resolutions
    keywords = ['Palestine', 'Israel', 'Middle East', 'Gaza']
    combined_text = (outcomes_filtered['title'].fillna('') + ' ' +
                     outcomes_filtered['subjects'].fillna('')).str.lower()
    keyword_mask = combined_text.str.contains('|'.join(keywords), case=False, na=False)
    outcomes_final = outcomes_filtered[keyword_mask].copy()

    resolution_ids = outcomes_final['resolution'].tolist()

    # Load voting.csv
    voting_df = pd.read_csv(voting_filepath)

    # Standardize vote values
    vote_mapping = {'Y': 1, 'N': -1, 'A': 0, 'Absent': 0, 'X': 0}
    voting_df['Vote_Value'] = voting_df['ms_vote'].str.upper().map(vote_mapping)

    # Filter voting data
    voting_filtered = voting_df[voting_df['resolution'].isin(resolution_ids)].copy()
    voting_filtered = voting_filtered.dropna(subset=['ms_name', 'resolution', 'Vote_Value'])

    # Create bipartite DataFrame
    df_bipartite = voting_filtered[['ms_name', 'resolution', 'Vote_Value']].copy()
    df_bipartite.columns = ['Country', 'Resolution_ID', 'Vote_Value']

    # Standardize Country column
    df_bipartite['Country'] = df_bipartite['Country'].str.upper().str.strip()

    # drop abstentions, they muddy the alliance network
    df_bipartite = df_bipartite[df_bipartite['Vote_Value'] != 0].copy()

    total_resolutions = df_bipartite['Resolution_ID'].nunique()

    print(f"Processed {len(df_bipartite)} definitive votes")
    print(f"Unique countries: {df_bipartite['Country'].nunique()}")
    print(f"Unique resolutions: {total_resolutions}")

    return df_bipartite, total_resolutions