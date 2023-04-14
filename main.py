"""
Module Name: Frontend App with Taipy GUI
Author: Kenneth Leung
Last Modified: 25 Mar 2023
"""
# Launch app with the command in CLI: python main.py
from src.config import *
from src.functions import *
from pages.analysis_md import *
from pages.data_viewer_md import *
import taipy as tp
from taipy.gui import Gui, Icon, navigate

with open('config.yml') as f:
    cfg = yaml.safe_load(f)

# =======================
#       Setup menu
# =======================
menu = [("Analysis", Icon('assets/histogram_menu_2.png', 'Analysis')),
        ('Data', Icon('assets/data_menu.png', 'Data'))]

page_markdown = """
<|toggle|theme|>
<|menu|label=Menu|lov={menu}|on_action=menu_function|>
"""

pages = {"/":page_markdown,
         "Analysis":analysis_page,
         "Data":data_page}

def menu_function(state, var_name: str, fct: str, var_value: list):
    # Change the value of the state.page variable in order to render the correct page
    navigate(state, var_value["args"][0])

# Run application
if __name__ == "__main__":
    tp.Core().run()

    # Create and execute scenario
    scenario_selector = [(s.id, s.name) for s in tp.get_scenarios()]
    scenario = tp.create_scenario(scenario_cfg, name="Default Scenario")
    selected_scenario = scenario.id
    tp.submit(scenario)

    df = scenario.pipeline_keyword_analysis.data_keywords_df.read()
    df_keywords_count = scenario.pipeline_keyword_analysis.data_keywords_count.read()

    Gui(pages=pages).run(title="Keyword Extraction and Analysis with KeyBERT and Taipy", 
                         dark_mode=False, 
                         port=8020, 
                         use_reloader=True)
