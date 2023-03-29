"""
Module Name: Core Functions (Backend)
Author: Kenneth Leung
Last Modified: 19 Mar 2023
"""
import arxiv
import pandas as pd
from keybert import KeyBERT
import yaml

with open('config.yml') as f:
    cfg = yaml.safe_load(f)

def extract_arxiv(query: str):
    search = arxiv.Search(
                query=query,
                max_results=cfg['MAX_ABSTRACTS'], # Limit number of abstracts
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )
     
    # Returns arxiv object
    return search


def save_in_dataframe(search):
    df = pd.DataFrame([{'uid': result.entry_id.split('.')[-1],
                        'title': result.title,
                        'date_published': result.published,
                        'abstract': result.summary} for result in search.results()])
    return df


def preprocess_data(df: pd.DataFrame):
    df['date_published'] = pd.to_datetime(df['date_published'])

    # Create empty column to store keyword extraction output
    df['keywords_and_scores'] = ''

    # Create empty column to store top keywords
    df['keywords'] = ''

    return df


def run_keybert(df: pd.DataFrame, ngram_min: int, ngram_max: int, diversity_algo: str, top_n: int, diversity: float, nr_candidates: int):
    kw_model = KeyBERT(model='all-MiniLM-L6-v2')
    use_mmr = diversity_algo.lower() == 'mmr'
    use_maxsum = diversity_algo.lower() == 'maxsum'
    
    for i, row in df.iterrows():
        abstract_text = row['abstract']
        kw_output = kw_model.extract_keywords(abstract_text,
                                              keyphrase_ngram_range=(ngram_min, ngram_max),
                                              stop_words='english',
                                              use_mmr=use_mmr,
                                              use_maxsum=use_maxsum,
                                              top_n=top_n,
                                              diversity=diversity,
                                              nr_candidates=nr_candidates)
        df.at[i, 'keywords_and_scores'] = kw_output
        df.at[i, 'keywords'] = [pair[0] for pair in kw_output]
    return df


def get_keyword_value_counts(df):
    keywords_count = pd.Series(df['keywords'].explode()).value_counts().reset_index()
    keywords_count.columns = ['keyword', 'count']

    return keywords_count


