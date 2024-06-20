from enum import Enum
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output

score_board = {}

step_limit = {
    "demo": 15,
    "beginner1": 15,
    "beginner2": 15,
    "ultimate": 50
}

full_score = {
    "beginner1": 4,
    "beginner2": 6,
    "ultimate": 10
}

maze_demo_str = """#####
#000E
#0###
#0###
#B###"""

maze_beginner_str_1 = """#E#####
#0#000#
#0#B#0#
#0###0#
#00000#
#######"""

maze_beginner_str_2 = """#####E#
#000#0#
#0#B#0#
#0###0#
#00000#
#######"""

maze_ultimate_str = """############
#00#0000000#
E0##0#0##0##
#0000#00#00#
#0####0#####
#0##0000000#
#0000#####0#
#####0000#0#
#000#0##000#
#000#0##0#0#
#0#00000000#
#B##########"""


class Cardinal(Enum):
    WEST = 1
    EAST = 2
    NORTH = 3
    SOUTH = 4


def find_adjacent_way(maze, pos):
    row = pos[0]
    col = pos[1]
    # Check the four adjacent cells
    if row > 0 and maze[row - 1][col] == 1:
        return (row - 1, col)
    if row < len(maze) - 1 and maze[row + 1][col] == 1:
        return (row+1, col)
    if col > 0 and maze[row][col - 1] == 1:
        return (row, col-1)
    if col < len(maze[0]) - 1 and maze[row][col + 1] == 1:
        return (row, col+1)

class Bot:
    __step = 0
    __pos = None
    __cardinal = None
    maze = None

    def __init__(self, maze):
        row, col = np.where(maze == 2)
        self.maze = maze
        self.__pos = [row, col]
        if row > 0 and maze[row - 1, col] == 0:
            self.__cardinal = Cardinal.NORTH
        if row < len(maze) - 1 and maze[row + 1, col] == 0:
            self.__cardinal = Cardinal.SOUTH
        if col > 0 and maze[row, col - 1] == 0:
            self.__cardinal = Cardinal.WEST
        if col < len(maze[0]) - 1 and maze[row, col + 1] == 0:
            self.__cardinal = Cardinal.EAST

    def move(self):
        self.__step += 1
        if self.can_move():
            if self.__cardinal == Cardinal.NORTH:
                self.__pos[0] -= 1
            elif self.__cardinal == Cardinal.SOUTH:
                self.__pos[0] += 1
            elif self.__cardinal == Cardinal.WEST:
                self.__pos[1] -= 1
            elif self.__cardinal == Cardinal.EAST:
                self.__pos[1] += 1

    def can_move(self):
        if self.__cardinal == Cardinal.NORTH:
            return self.__pos[0] - 1 >= 0 and self.maze[self.__pos[0] - 1, self.__pos[1]] != 1
        elif self.__cardinal == Cardinal.SOUTH:
            return self.__pos[0] + 1 < len(self.maze) and self.maze[self.__pos[0] + 1, self.__pos[1]] != 1
        elif self.__cardinal == Cardinal.WEST:
            return self.__pos[1] - 1 >= 0 and self.maze[self.__pos[0], self.__pos[1] - 1] != 1
        elif self.__cardinal == Cardinal.EAST:
            return self.__pos[1] + 1 < len(self.maze[0]) and self.maze[self.__pos[0], self.__pos[1] + 1] != 1
        else:
            return False

    def turn(self, cardinal):
        self.__cardinal = cardinal

    def get_step(self):
        return self.__step

    def reset_step(self):
        self.__step = 0

    def get_y(self):
        return self.__pos[0]

    def get_x(self):
        return self.__pos[1]

    def get_cardinal(self):
        return self.__cardinal


def generate_2d_maze(maze_str):
    maze_lines = maze_str.splitlines()
    maze_array = []
    for line in maze_lines:
        row = []
        for char in line:
            if char == '0':
                row.append(0)
            elif char == '#':
                row.append(1)
            elif char == 'B':
                row.append(2)
            elif char == 'E':
                row.append(3)
        maze_array.append(row)
    return np.array(maze_array)


def only_one_step(bot):
    return bot.get_step() <= 1


def draw_maze(maze, bot=None):
    clear_output(wait=True)
    maze_copy = np.copy(maze)
    if bot is not None:
        maze_copy[np.where(maze == 2)] = 0
        maze_copy[bot.get_y(), bot.get_x()] = 2
        bot.reset_step()
    fig, ax = plt.subplots(figsize=(len(maze_copy) * 0.5, len(maze_copy[0]) * 0.5))

    cmap = plt.get_cmap("binary")
    cmap.set_under(color="black")
    cmap.set_over(color="red")

    ax.imshow(maze_copy, cmap=cmap, vmin=0, vmax=3)
    ax.axis("off")

    plt.pause(0.1)
    plt.close(fig)


def finish(maze, bot):
    return maze[bot.get_y(), bot.get_x()] == 3


def run_maze(maze, run, score_key, demo = False):
    counter = 0
    bot = Bot(maze)
    while counter < step_limit[score_key]:
        run(bot)
        if bot.get_step() > 1:
            raise Exception("You cannot ask the bot to move two steps in one round. It's gonna be exhausting 3_3)")
        draw_maze(maze, bot)
        counter += 1
        if finish(maze, bot):
            if demo:
                print("That is how a maze master does things!")
            else:
                score_board[score_key] = full_score[score_key]
                print(f'Thank you! You are doing a great job! Here is your {full_score[score_key]} points.')
            break
    if not finish(maze, bot):
        score_board[score_key] = 0
        print(f'Sorry you failed to help the bot within {step_limit[score_key]} steps...')


maze_demo = generate_2d_maze(maze_demo_str)
maze_beginner_1 = generate_2d_maze(maze_beginner_str_1)
maze_beginner_2 = generate_2d_maze(maze_beginner_str_2)
maze_ultimate = generate_2d_maze(maze_ultimate_str)


def show_scoreboard():
    print("Here is your scores for the games:")
    print(f'Beginner Maze 1: {score_board["beginner1"]}')
    print(f'Beginner Maze 2: {score_board["beginner2"]}')
    print(f'Ultimate Maze: {score_board["ultimate"]}')