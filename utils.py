"""
Module Name: Functions (Utils)
Author: Kenneth Leung
Last Modified: 12 Mar 2023
"""

import arxiv
import pandas as pd
from keybert import KeyBERT

def extract_arxiv(query: str, 
                  max_results: int):
    search = arxiv.Search(
                query = query,
                max_results = max_results,
                sort_by = arxiv.SortCriterion.SubmittedDate,
                sort_order = arxiv.SortOrder.Descending
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
                stop_words: str or None, 
                ngram_min: int, 
                ngram_max: int,
                fine_tune_method: str, 
                diversity: float, 
                top_n: int):
    for i, row in df.iterrows():
        kw_model = KeyBERT(model='all-MiniLM-L6-v2')
        abstract_text = row['abstract']
        if fine_tune_method == 'MMR':
            use_mmr, use_maxsum = True, False
        else:
            use_mmr, use_maxsum = False, True

        kw_output = kw_model.extract_keywords(abstract_text, 
                                    keyphrase_ngram_range=(ngram_min, ngram_max), 
                                    stop_words=stop_words,
                                    use_mmr=use_mmr, 
                                    use_maxsum=use_maxsum,
                                    diversity=diversity,
                                    top_n=top_n)
        df.at[i, 'keywords_and_scores'] = kw_output
        
        # Obtain keyword from every keyword-score pair
        top_kw = []
        for pair in kw_output:
            top_kw.append(pair[0])
            
        df.at[i, 'keywords'] = top_kw

    return df


# def set_sqlite_connection(data_path, db_name):
#     if not os.path.exists(data_path):
#             os.makedirs(data_path)  
#     connection = sqlite3.connect(f"{data_path}/{db_name}.db")
#     return connection

# def create_sqlite_table(connection, table_name):
#     cursor = connection.cursor()
#     # Create new table in database
#     cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id TEXT PRIMARY KEY, \
#                                                              title TEXT, \
#                                                              date_published TEXT, \
#                                                              abstract TEXT)"
#                   )

# def save_results_in_sqlite(connection, table_name, search):
#     cursor = connection.cursor()   
#     for result in search.results():
#         entry_id = result.entry_id
#         uid = entry_id.split('.')[-1]
#         title = result.title
#         date_published = result.published
#         abstract = result.summary
        
#         query = f'INSERT OR REPLACE INTO {table_name}(id, title, date_published, abstract)' + \
#                  ' VALUES(?, ?, ?, ?);'
#         fields = (uid, title, date_published, abstract)
#         cursor.execute(query, fields)
