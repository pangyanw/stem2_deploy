import ipywidgets as widgets

styles = '🔴🟢🔵🟡⚫🟠⚪🟣🟤⭕'

chances = 10
guess = [0, 0, 0, 0]
guesses = []
colors = 4
truth = [1, 2, 3, 4]
responses = []

board = widgets.HTML(value='')
message = widgets.HTML()

def get_on_change(index):
    def on_change(change):
        if change['type'] == 'change' and change['name'] == 'value':
            value = change['new']
            guess[index] = styles.index(value)

    return on_change

def render_row(guess, response):
    if response[0] == colors:
        message.value = 'you won, congratulations!'
    guess_circles = [styles[g] for g in guess]
    response_circles = ''.join((['🟢'] * response[0] + ['🟡'] * response[1] + ['⚪'] * colors)[:colors])
    return f'''
    <div style="display: flex;align-items: center;">
    <div style="height: 50px; font-size: 38px; line-height: 50px; margin-right: 16px">{''.join(guess_circles)}</div>
    <div stule="font-size: 25px;">
    {response_circles}
    </div>
    </div>
    '''


def render(guesses, responses):
    if len(guesses) < len(responses):
        return
    rows = [
        render_row(guess, response)
        for guess, response in zip(guesses, responses)
    ]
    html = f'''
{''.join(rows)}
'''
    board.value = html


def handle_new_game(random_unique):
    global guesses, responses, truth
    guesses = []
    responses = []
    truth = random_unique(colors)
    message.value = ''
    render(guesses, responses)


def handle_submit(calculate_green, calculate_yellow):
    response = [
        calculate_green(guess, truth),
        calculate_yellow(guess, truth)
    ]
    guesses.append([*guess])
    responses.append(response)
    render(guesses, responses)



def start_game(calculate_green, calculate_yellow, random_unique, colors_length=4):
    global colors, guess
    colors = colors_length

    selects = [widgets.Dropdown(
        options=[it for it in styles],
        description='',
        layout=widgets.Layout(width='50px'))
        for _ in range(colors)]
    submit_button = widgets.Button(description='submit')
    new_game_button = widgets.Button(description='new game')

    guess = [0] * colors
    

    for i in range(colors):
        selects[i].observe(get_on_change(i))

    new_game_button.on_click(lambda _: handle_new_game(random_unique))
    submit_button.on_click(lambda _: handle_submit(calculate_green, calculate_yellow))
    vbox = widgets.VBox([
        widgets.HBox([new_game_button, message]),
        widgets.HBox(selects + [submit_button]),
        board
    ])
    handle_new_game(random_unique)
    return vbox