"""
Module Name: Page Markdown Template (Analysis Page)
Author: Kenneth Leung
Last Modified: 8 Apr 2023
"""
import taipy as tp
from taipy.gui import notify
from src.config import scenario_cfg

import yaml
with open('config.yml') as f:
    cfg = yaml.safe_load(f)

query = cfg['QUERY']
ngram_min = cfg['NGRAM_MIN']
ngram_max = cfg['NGRAM_MAX']
diversity_algo = cfg['DIVERSITY_ALGO']
diversity_algo_options = ['mmr', 'maxsum']
diversity = cfg['DIVERSITY']
top_n = cfg['TOP_N']
nr_candidates = cfg['NR_CANDIDATES']


# Input section of dashboard
input_page = """
# Keyword Extraction and Analysis with KeyBERT and Taipy

<br/>

<|layout|columns=1 1 1 1 1 1 1|
<|{query}|input|label=Query Topic|>

<|{ngram_min}|number|label=Min N-gram|>

<|{ngram_max}|number|label=Max N-gram|>

<|{top_n}|number|label=Top n results|>

<|{diversity}|number|label=Diversity (for MMR)|>

<|{nr_candidates}|number|label=No. of Candidates (for MaxSum)|>

<|{diversity_algo}|selector|lov={diversity_algo_options}|dropdown|label=Diversity Algorithm|>

<|Update Analysis|button|on_action=submit_scenario|>
|>
<br/> 
<br/> 

<|{selected_scenario}|selector|lov={scenario_selector}|dropdown|label=Scenario|on_change=synchronize_gui_core|value_by_id|> 

<|Save Scenario|button|on_action=create_scenario|> 

<br/>

"""

# Chart types: https://docs.taipy.io/en/latest/manuals/gui/viselements/chart/
chart_properties = {"type":"bar",
                    "y":"keyword",
                    "x":"count",
                    "orientation": "h",
                    "layout": {
                        "xaxis": {"title": "Frequency Count"},
                        "yaxis": {"title": None},
                        "showlegend": False, # Hide the legend
                        "title": 'Keyword Frequency Bar Plot',
                        "margin": {'pad': 0}
                        }
                }

# Output section of dashboard
output_page = """
<|layout|columns=1 1|gap=10px|
<|{df_keywords_count}|table|width=30|page_size=10|height=20|>

<|{df_keywords_count}|chart|properties={chart_properties}|height=20|>
|>

"""

# Combine layout segments
analysis_page = input_page + output_page


# ======= Scenario Setup =========
def create_scenario(state):
    print("Creating scenario...")
    scenario = tp.create_scenario(scenario_cfg, name=f"Scenario N {len(state.scenario_selector)} {state.query}")
    state.scenario_selector += [(scenario.id, scenario.name)]
    state.selected_scenario = scenario.id
    notify(state, 'success', 'Scenario created!')
    submit_scenario(state)


def update_chart(state):
    # Select the right scenario and pipeline
    scenario = tp.get(state.selected_scenario)
    # Update the chart based on this pipeline
    state.df = scenario.pipeline_keyword_analysis.data_keywords_df.read()
    state.df_keywords_count = scenario.pipeline_keyword_analysis.data_keywords_count.read()


def submit_scenario(state):
     print("Submitting scenario...")
     notify(state, 'info', 'Submitting scenario...')
     # Get the selected scenario: in this current step a single scenario is created then modified here.
     scenario = tp.get(state.selected_scenario)

     # Change the default parameters by writing in the datanodes
     scenario.query.write(str(state.query))
     scenario.ngram_max.write(int(state.ngram_max))
     scenario.diversity_algo.write(str(state.diversity_algo))
     scenario.diversity.write(float(state.diversity))
     scenario.top_n.write(int(state.top_n))
     scenario.nr_candidates.write(int(state.nr_candidates))

     # Execute the pipelines/code
     tp.submit(scenario)
     notify(state, 'success', 'Execution finished!')
     # Update the chart when we change the scenario
     update_chart(state)


def synchronize_gui_core(state):
    scenario = tp.get(state.selected_scenario)
    # get the information of the selected scenario and display it on the GUI
    state.query = scenario.query.read()
    state.ngram_max = scenario.ngram_max.read()
    state.diversity_algo = scenario.diversity_algo.read()
    state.diversity = scenario.diversity.read()
    state.top_n = scenario.top_n.read()
    state.nr_candidates = scenario.nr_candidates.read()
    update_chart(state)
