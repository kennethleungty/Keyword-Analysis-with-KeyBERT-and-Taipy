"""
Module Name: Taipy Configurations
Author: Kenneth Leung
Last Modified: 19 Mar 2023
"""

import yaml
from taipy import Config, Scope
from src.core import *

with open('config.yml') as f:
    cfg = yaml.safe_load(f)

# ====================
#   Input Data Nodes
# ====================
# To place input values as DataNodeConfig objects
data_query_cfg = Config.configure_data_node(id='query', default_data=cfg['QUERY'])
data_ngram_min_cfg = Config.configure_data_node(id='ngram_min', default_data=cfg['NGRAM_MIN'])
data_ngram_max_cfg = Config.configure_data_node(id='ngram_max', default_data=cfg['NGRAM_MAX'])
data_diversity_algo_cfg = Config.configure_data_node(id='diversity_algo', default_data=cfg['DIVERSITY_ALGO'])
data_top_n_cfg = Config.configure_data_node(id='top_n', default_data=cfg['TOP_N'])
data_diversity_cfg = Config.configure_data_node(id='diversity', default_data=cfg['DIVERSITY'])
data_nr_candidates_cfg = Config.configure_data_node(id='nr_candidates', default_data=cfg['NR_CANDIDATES'])

# ===================
#   Key Data Nodes
# ===================
data_arxiv_search_cfg = Config.configure_data_node(id='data_arxiv_search', 
                                                   scope=Scope.GLOBAL,
                                                   cacheable=True)
data_raw_df_cfg = Config.configure_data_node(id='data_raw_df',
                                             scope=Scope.GLOBAL,
                                             cacheable=True)
data_processed_df_cfg = Config.configure_data_node(id='data_processed_df',
                                                   scope=Scope.GLOBAL,
                                                   cacheable=True)
data_keywords_df_cfg = Config.configure_data_node(id='data_keywords_df',
                                                  scope=Scope.GLOBAL,
                                                  cacheable=True)

data_keywords_count_cfg = Config.configure_data_node(id='data_keywords_count',
                                                     scope=Scope.GLOBAL,
                                                     cacheable=True)

# =================
#      Tasks
# =================
task_arxiv_extraction_cfg = Config.configure_task(id="task_arxiv_extraction",
                                                  function=extract_arxiv,
                                                  input=data_query_cfg,
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
                                                         data_ngram_min_cfg,
                                                         data_ngram_max_cfg, 
                                                         data_diversity_algo_cfg, 
                                                         data_top_n_cfg,
                                                         data_diversity_cfg, 
                                                         data_nr_candidates_cfg],
                                                  output=data_keywords_df_cfg)

task_get_kw_count_cfg = Config.configure_task(id='task_count_keywords',
                                                  function=get_keyword_value_counts,
                                                  input=data_keywords_df_cfg,
                                                  output=data_keywords_count_cfg)


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
                                                          task_configs=[task_extract_keywords_cfg,
                                                                        task_get_kw_count_cfg
                                                                        ])

# =============
#   Scenario 
# =============
scenario_cfg = Config.configure_scenario(id="scenario", 
                                         pipeline_configs=[pipeline_data_prep_cfg, 
                                                           pipeline_keyword_analysis_cfg
                                                           ])
