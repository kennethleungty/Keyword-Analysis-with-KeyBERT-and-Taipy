"""
Module Name: Frontend App with Taipy GUI
Author: Kenneth Leung
Last Modified: 12 Mar 2023
"""

import taipy as tp

# Initial value
n_week = 10

# Get last n articles
# Display word cloud
# Bar chart to show top x keywords
# 

# prompt_user = gui.add_partial(
# """
# Enter a name:

# <|{name}|input|>
# """
# )

analysis_page = """
# Getting started with *Taipy*

# Create your scenario
<|layout|columns=1 1 1 1|
<|
**Prediction date**\n\n <|{day}|date|not with_time|>
|>
<|
**Max capacity**\n\n <|{max_capacity}|number|>
|>
<|
**Number of predictions**\n\n<|{n_predictions}|number|>
|>
<|
<br/> <br/>\n <|Create new scenario|button|on_action=create_scenario|>
|>
|>
<|part|render={len(scenario_selector) > 0}|
<|layout|columns=1 1|
<|
## Scenario \n <|{selected_scenario}|selector|lov={scenario_selector}|dropdown|>
|>
<|
## Display the pipeline \n <|{selected_pipeline}|selector|lov={pipeline_selector}|dropdown|>
|>
|>
<|{predictions_dataset}|chart|x=Date|y[1]=Historical values|type[1]=bar|y[2]=Predicted values|type[2]=scatter|height=80%|width=100%|>
|>
"""


data_page = '''
# Abstracts here
'''

lov_menu = [("Analysis", "Analysis"),
            ("Data", "Data")]

# Create a menu with our pages
root_md = "<|menu|label=Menu|lov={lov_menu}|on_action=menu_fct|>"

pages = {"/":root_md,
         "Analysis":analysis_page,
         "Data":data_page}


def menu_fct(state, var_name: str, fct: str, var_value: list):
    # Change the value of the state.page variable in order to render the correct page
    tp.gui.navigate(state, var_value["args"][0])


if __name__ == "__main__":
    gui = tp.Gui(pages=pages)
    core = tp.Core()
    tp.run(gui, core, title="Taipy Demo", dark_mode=False, port=8020)