"""
Module Name: Backend Pipeline with Taipy Core
Author: Kenneth Leung
Last Modified: 12 Mar 2023
"""

from utils import *
from config import *
from taipy import Config, Scope

# ===================
#     Data Nodes 
# ===================
arxiv_search_results_cfg = Config.configure_data_node(id='search_results',
                                                      scope=Scope.GLOBAL)

raw_dataframe_cfg = Config.configure_data_node(id='df_raw',
                                               scope=Scope.PIPELINE)

processed_dataframe_cfg = Config.configure_data_node(id='df_processed',
                                                     scope=Scope.PIPELINE)

keywords_dataframe_cfg = Config.configure_data_node(id='df_keywords',
                                                    scope=Scope.PIPELINE)

# =================
#      Tasks
# =================
arxiv_extraction_task_cfg = Config.configure_task(id="arxiv_api_search",
                                                  function=extract_arxiv,
                                                  input=[QUERY, MAX_RESULTS],
                                                  output=arxiv_search_results_cfg)

save_in_dataframe_task_cfg = Config.configure_task(id="save_dataframe",
                                                   function=save_in_dataframe,
                                                   input=arxiv_search_results_cfg,
                                                   output=raw_dataframe_cfg)

process_data_task_cfg = Config.configure_task(id='preprocess_data',
                                              function=preprocess_data,
                                              input=raw_dataframe_cfg,
                                              output=processed_dataframe_cfg)

extract_keywords_task_cfg = Config.configure_task(id='extract_keywords',
                                              function=run_keybert,
                                              input=[processed_dataframe_cfg, STOP_WORDS, 
                                                     NGRAM_MIN, NGRAM_MAX, FINE_TUNE_METHOD, 
                                                     DIVERSITY, TOP_N],
                                              output=keywords_dataframe_cfg)


# Also need a set of display configs (output bar chart and word cloud)

# =================
#    Pipelines
# =================


def run_pipeline(query, max_results, stop_words, ngram_min, ngram_max, 
                 fine_tune_method, diversity, top_n):
    search = extract_arxiv(query, max_results)
    df_raw = save_in_dataframe(search)
    df_processed = preprocess_data(df_raw)
    df_final = run_keybert(df_processed, stop_words, ngram_min, ngram_max,
                           fine_tune_method, diversity, top_n)

    print(df_final)



# TODO: Split pipeline so that the initial extraction does not change unless number of articles change
# Don't re-extract when other variables related to KeyBert are amended

# # Test pipeline run
# run_pipeline(QUERY, MAX_RESULTS, STOP_WORDS, NGRAM_MIN, NGRAM_MAX, 
#              FINE_TUNE_METHOD, DIVERSITY, TOP_N)
