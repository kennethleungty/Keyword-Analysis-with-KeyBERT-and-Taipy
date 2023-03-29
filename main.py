"""
Module Name: Frontend App with Taipy GUI
Author: Kenneth Leung
Last Modified: 25 Mar 2023
"""
# Launch app with the command in CLI: python main.py

from src.config import *
from src.functions import *
from src.utils import *
from pages.analysis_md import *
from pages.dataframe_md import *

import taipy as tp
from taipy.gui import Gui, Icon, navigate

with open('config.yml') as f:
    cfg = yaml.safe_load(f)

# =======================
#       Setup menu
# =======================
menu_lov = [("Analysis", Icon('assets/histogram_menu.svg', 'Analysis')),
            ('Data', Icon('assets/Datanode.svg', 'Data'))]

page_markdown = """
<|toggle|theme|>
<|menu|label=Menu|lov={menu_lov}|on_action=menu_fct|>
"""

pages = {"/":page_markdown,
         "Analysis":analysis_page,
         "Data":data_page}

def menu_fct(state, var_name: str, fct: str, var_value: list):
    # Change the value of the state.page variable in order to render the correct page
    navigate(state, var_value["args"][0])



# Run application
if __name__ == "__main__":
    tp.Core().run()

    # Create and execute scenario
    scenario = tp.create_scenario(scenario_cfg, name="First Scenario")
    selected_scenario = scenario.id
    tp.submit(scenario)

    scenario_selector = [(s.id, s.name) for s in tp.get_scenarios()]

    df = scenario.pipeline_keyword_analysis.data_keywords_df.read()
    df_keywords_count = scenario.pipeline_keyword_analysis.data_keywords_count.read()

    Gui(pages=pages).run(title="Taipy Demo 123", 
                         dark_mode=False, 
                         port=8020, 
                         use_reloader=True)


"""
TO CONTINUE
- Figure out change graphs when selected parameters change
- How NOT to reload abstracts, but just work on the analysis
- Set min max values of paramerters 
- Currently keywords all stuck together (in dataframe), sort that out (explore in notebooks)

DONE
- How come the task for task_keyword_cfg cannot run when placed in separate pipeline in the same scenario?
 Able to run when all tasks are in a single pipeline. ANS: Scope needs to be set as global
 - Build the visualizations

"""