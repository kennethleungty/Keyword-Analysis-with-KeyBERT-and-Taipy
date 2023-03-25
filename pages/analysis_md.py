"""
Module Name: Page Markdown Template (Analysis Page)
Author: Kenneth Leung
Last Modified: 19 Mar 2023
"""
import yaml
with open('config.yml') as f:
    cfg = yaml.safe_load(f)

query = cfg['QUERY']
ngram_max = cfg['NGRAM_MAX']
fine_tune = cfg['FINE_TUNE_METHOD']
fine_tune_options = ['mmr', 'maxsum']
diversity = cfg['DIVERSITY']
top_n = cfg['TOP_N']
nr_candidates = cfg['NR_CANDIDATES']

# Chart types: https://docs.taipy.io/en/latest/manuals/gui/viselements/chart/
chart_properties = {"type":"bar",
                    "y":"keyword",
                    "x":"count",
                    "orientation": "h",
                    "layout": {
                        "barmode": "overlay",
                        # Set a relevant title for axes
                        "xaxis": { "title": "Frequency Count"},
                        "yaxis": { "title": None},
                        "showlegend": False, # Hide the legend
                        "title": None,
                        "margin": {'pad': -15}
                        }
                }


analysis_page = """
# Keyword Analysis

This is some placeholder text

<br/>

<|layout|columns=1 1 1 1 1 1|gap=0px|
<|
<|{query}|input|label=Query Topic|>
|>
<|
<|{ngram_max}|number|label=Max N-gram|>
|>
<|
<|{top_n}|number|label=Top n results|>
|>
<|
<|{diversity}|number|label=Diversity (for MMR)|>
|>
<|
<|{nr_candidates}|number|label=NR Candidates (for MaxSum)|>
|>
<|
<|{fine_tune}|selector|lov={fine_tune_options}|dropdown|label=Fine-tune Method|>
|>
|>

<|
<br/> 
<|Update Analysis|button|on_action=submit_scenario|>
|>
<br/>

<|layout|columns=1 1|gap=10px|
<|
<|{df_keywords_count}|table|width=30|page_size=10|height=5|>
|>
<|
<|{df_keywords_count}|chart|properties={chart_properties}|height=80|>
|>
|>
"""