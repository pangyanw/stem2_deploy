import ipywidgets as widgets

items = [widgets.HTML(" ") for _ in range(16)]
result_label = widgets.Label(" ")
empty_label = widgets.Label(" ")


LEFT = "←"
RIGHT = "→"
UP = "↑"
DOWN = "↓"


style = {
    # color, background-color, font-size
    None: ('#776e65', '#CDC1B4', '50px'),
    2: ('#776e65', '#eee4da', '50px'),
    4: ('#776e65', '#eee1c9', '50px'),
    8: ('#f9f6f2', '#f3b27a', '50px'),
    16: ('#f9f6f2', '#f69664', '50px'),
    32: ('#f9f6f2', '#f77c5f', '50px'),
    64: ('#f9f6f2', '#f75f3b', '50px'),
    128: ('#f9f6f2', '#edd073', '50px'),
    256: ('#f9f6f2', '#edcc62', '50px'),
    512: ('#f9f6f2', '#edc950', '50px'),
    1024: ('#f9f6f2', '#edc53f', '35px'),
    2048: ('#f9f6f2', '#edc22e', '35px'),
    4096: ('#f9f6f2', '#edc22e', '35px'),
    9182: ('#f9f6f2', '#edc22e', '35px'),
    9182 * 2: ('#f9f6f2', '#edc22e', '30px'),
}

global_grid = None
global_result = None

def render(grid, result_text):
    result_label.value = result_text
    for rowid, row in enumerate(grid):
        for colid, col in enumerate(row):
            color, background, fontsize = style[col]
            css = f"""
            color: {color};
            background-color: {background};
            font-size: {fontsize};
            text-align: center;
            border: solid 1px grey;
            width: 100px;
            height: 100px;
            line-height: 100px;
            """
            items[rowid * 4 + colid].value = f'<div style="{css}">{col if col is not None else " "}</div>'


def set_game_state(grid, result):
    global global_grid, global_result
    global_grid = grid
    global_result = result
    render(grid, result if result is not None else '')

def enrich_arrow_handler(on_arrow_button_clicked, direction):
    def wrapped_handler(_):
        next_state = on_arrow_button_clicked(global_grid, direction)
        set_game_state(next_state["grid"], next_state["result"])

    return wrapped_handler

def enrich_new_game_handler(on_new_game_button_clicked):
    def wrapped_handler(_):
        next_state = on_new_game_button_clicked()
        set_game_state(next_state["grid"], next_state["result"])

    return wrapped_handler



def start_game(on_new_game_button_clicked, on_arrow_button_clicked):
    new_game_button = widgets.Button(description="New Game")
    new_game = enrich_new_game_handler(on_new_game_button_clicked)
    new_game_button.on_click(new_game)
    new_game(None)

    left_button = widgets.Button(description=LEFT)
    left_button.on_click(enrich_arrow_handler(on_arrow_button_clicked, LEFT))

    right_button = widgets.Button(description=RIGHT)
    right_button.on_click(enrich_arrow_handler(on_arrow_button_clicked, RIGHT))

    up_button = widgets.Button(description=UP)
    up_button.on_click(enrich_arrow_handler(on_arrow_button_clicked, UP))

    down_button = widgets.Button(description=DOWN)
    down_button.on_click(enrich_arrow_handler(on_arrow_button_clicked, DOWN))

    hbox = widgets.VBox([
        widgets.HBox([new_game_button, up_button]),
        widgets.HBox([left_button, down_button, right_button]),
        result_label,
        widgets.HBox([items[0], items[1], items[2], items[3]]),
        widgets.HBox([items[4], items[5], items[6], items[7]]),
        widgets.HBox([items[8], items[9], items[10], items[11]]),
        widgets.HBox([items[12], items[13], items[14], items[15]]),
    ])
    return hbox