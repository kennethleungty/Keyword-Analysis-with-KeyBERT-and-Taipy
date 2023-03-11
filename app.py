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

main_page = '''
# Getting started with *Taipy*
<|navbar|>


<|open |pane|anchor=left| partial={partial} >

*<|{n_week}|>*
<|{n_week}|slider|min=1|max=52|>

<|{show_dialog}|dialog|
    ...
    <|{some content}|>
    ...
|>

'''

abstracts_page = '''
<|navbar|>

# Abstracts here
'''

pages = {
    "main": main_page,
    "abstracts": abstracts_page,
   }

if __name__ == "__main__":
    gui = tp.Gui(pages=pages)



    core = tp.Core()
    tp.run(gui, core, title="Taipy Demo", dark_mode=False, port=8020)