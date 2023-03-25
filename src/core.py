"""
Module Name: Core Functions (Backend)
Author: Kenneth Leung
Last Modified: 19 Mar 2023
"""
import arxiv
import pandas as pd
from keybert import KeyBERT
import taipy as tp
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
    df_raw = pd.DataFrame()

    for result in search.results():
        entry_id = result.entry_id
        uid = entry_id.split('.')[-1]
        title = result.title
        date_published = result.published
        abstract = result.summary
        
        result_dict = {'uid': uid,
                       'title': title,
                       'date_published': date_published,
                       'abstract': abstract
                    }
        df_raw = df_raw.append(result_dict, ignore_index=True)

    return df_raw


def preprocess_data(df: pd.DataFrame):
    df['date_published'] = pd.to_datetime(df['date_published'])

    # Create empty column to store keyword extraction output
    df['keywords_and_scores'] = ''

    # Create empty column to store top keywords
    df['keywords'] = ''

    return df


def run_keybert(df: pd.DataFrame, 
                ngram_max: int,
                fine_tune_method: str, 
                top_n: int,
                diversity: float, 
                nr_candidates: int
                ):
    for i, row in df.iterrows():
        kw_model = KeyBERT(model='all-MiniLM-L6-v2')
        abstract_text = row['abstract']
        if fine_tune_method.lower() == 'mmr':
            use_mmr, use_maxsum = True, False
        elif fine_tune_method.lower() == 'maxsum':
            use_mmr, use_maxsum = False, True

        kw_output = kw_model.extract_keywords(abstract_text, 
                                    keyphrase_ngram_range=(1, ngram_max), 
                                    stop_words='english',
                                    use_mmr=use_mmr, 
                                    use_maxsum=use_maxsum,
                                    top_n=top_n,
                                    diversity=diversity,
                                    nr_candidates=nr_candidates
                                    )
        df.at[i, 'keywords_and_scores'] = kw_output
        
        # Obtain keyword from every keyword-score pair
        top_kw = []
        for pair in kw_output:
            top_kw.append(pair[0])
        df.at[i, 'keywords'] = top_kw

    return df


def create_and_submit_pipeline(pipeline_cfg):
    pipeline = tp.create_pipeline(pipeline_cfg)
    tp.submit(pipeline)
    return pipeline


def get_keyword_value_counts(df):
    keywords_count = pd.DataFrame(pd.Series([x for item in df['keywords'] for x in item]).value_counts()).reset_index()
    keywords_count.columns = ['keyword', 'count']

    return keywords_count
