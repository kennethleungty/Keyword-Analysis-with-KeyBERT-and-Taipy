"""
Module Name: Backend Pipeline with Taipy Core
Author: Kenneth Leung
Last Modified: 12 Mar 2023
"""

from functions import *
from input import *
import taipy as tp
from taipy import Config, Scope

# ====================
#  Input Data Nodes
# ====================
# To place input values as DataNodeConfig objects
data_query_cfg = Config.configure_data_node(id='query', default_data=QUERY)
data_max_results_cfg = Config.configure_data_node(id='max_results', default_data=MAX_RESULTS)
data_stop_words_cfg = Config.configure_data_node(id='stop_words', default_data=STOP_WORDS)
data_ngram_min_cfg = Config.configure_data_node(id='ngram_min', default_data=NGRAM_MIN)
data_ngram_max_cfg = Config.configure_data_node(id='ngram_max', default_data=NGRAM_MAX)
data_fine_tune_cfg = Config.configure_data_node(id='fine_tune', default_data=FINE_TUNE_METHOD)
data_diversity_cfg = Config.configure_data_node(id='diversity', default_data=DIVERSITY)
data_top_n_cfg = Config.configure_data_node(id='top_n', default_data=TOP_N)


# ===================
#   Key Data Nodes
# ===================
data_arxiv_search_cfg = Config.configure_data_node(id='data_arxiv_search',
                                                   scope=Scope.GLOBAL)

data_raw_df_cfg = Config.configure_data_node(id='data_raw_df',
                                             scope=Scope.PIPELINE)

data_processed_df_cfg = Config.configure_data_node(id='data_processed_df',
                                                   scope=Scope.PIPELINE)

data_keywords_df_cfg = Config.configure_data_node(id='data_keywords_df',
                                                  scope=Scope.PIPELINE)

# =================
#      Tasks
# =================
task_arxiv_extraction_cfg = Config.configure_task(id="task_arxiv_extraction",
                                                  function=extract_arxiv,
                                                  input=[data_query_cfg, data_max_results_cfg],
                                                  output=data_arxiv_search_cfg,
                                                  skippable=True)

task_save_in_df_cfg = Config.configure_task(id="task_save_in_df",
                                            function=save_in_dataframe,
                                            input=data_arxiv_search_cfg,
                                            output=data_raw_df_cfg,
                                            skippable=True)

task_process_data_cfg = Config.configure_task(id='task_process_data',
                                              function=preprocess_data,
                                              input=data_raw_df_cfg,
                                              output=data_processed_df_cfg,
                                              skippable=True)

task_extract_keywords_cfg = Config.configure_task(id='task_extract_keywords',
                                              function=run_keybert,
                                              input=[data_processed_df_cfg, 
                                                     data_stop_words_cfg, 
                                                     data_ngram_min_cfg, 
                                                     data_ngram_max_cfg, 
                                                     data_fine_tune_cfg, 
                                                     data_diversity_cfg, 
                                                     data_top_n_cfg],
                                              output=data_keywords_df_cfg)


# Also need a set of display configs (output bar chart and word cloud)

# =================
#     Pipelines
# =================

# TODO: Split pipeline so that the initial extraction does not change unless number of articles change
# Don't re-extract when other variables related to KeyBert are amended

pipeline_data_prep_cfg = Config.configure_pipeline(id='pipeline_data_prep',
                                                   task_configs=[task_arxiv_extraction_cfg,
                                                                 task_save_in_df_cfg,
                                                                 task_process_data_cfg,
                                                                 ])

pipeline_keyword_analysis_cfg = Config.configure_pipeline(id='pipeline_keyword_analysis',
                                                      task_configs=[task_extract_keywords_cfg])



## Execute pipeline
if __name__ == "__main__":
    tp.Core().run()

    # Create the pipeline
    pipeline_data_prep = tp.create_pipeline(pipeline_data_prep_cfg)

    # Submit the pipeline (Execution)
    tp.submit(pipeline_data_prep)

    # Read output data from the pipeline (values from data node id attribute)
    df = pipeline_data_prep.data_processed_df.read()

    print(df)

# CONTINUE FROM HERE: HOw to Link GUI to Pipeline in Core: https://docs.taipy.io/en/latest/getting_started/getting-started/step_05/ReadMe/

# # Test pipeline run
# run_pipeline(QUERY, MAX_RESULTS, STOP_WORDS, NGRAM_MIN, NGRAM_MAX, 
#              FINE_TUNE_METHOD, DIVERSITY, TOP_N)
