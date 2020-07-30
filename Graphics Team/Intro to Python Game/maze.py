import os
import time
import queue

Compass = {
    "North": 0,
    "East": 1,
    "South": 2,
    "West": 3
}


def to_matrix(maze):
    matrix = []
    for s in maze:
        matrix.append(list(s))
    return matrix


class Maze:
    def __init__(self):
        self.maze = ["11111111111111",
                     "1 11         1",
                     "1  1 1 1 11111",
                     "1 11 1 1 11111",
                     "1  1 1 1 11111",
                     "11 1 1 1 11111",
                     "1  1 1 1 11111",
                     "11   1 1    11",
                     "1  1 111111  1",
                     "11 1     111 1",
                     "111  111   1E1",
                     "11111111111111"]
        self.player = Player()
        self.is_running = True


    def print_maze(self):
        if self.is_running:
            os.system('clear')
            for y in range(0, len(self.maze)):
                if self.is_running:
                    for x in range(0, len(self.maze[y])):
                        if self.player.x == x and self.player.y == y:
                            if self.maze[y][x] == "1":
                                print()
                                os.system('clear')
                                print("GAME OVER! YOU CRASHED INTO A WALL!")
                                print(self.player.history)
                                self.is_running = False
                                break
                            elif self.maze[y][x] == "E":
                                print()
                                os.system('clear')
                                print("YOU WIN! YOU GOT TO THE END!")
                                print(self.player.history)
                                self.is_running = False
                                break
                            else:
                                print(self.player.display_player(), end=' ')
                        else:
                            print(self.maze[y][x], end=" ")
                    print()


    def update(self):
        if self.is_running:
            self.player.bfs([
                self.maze[self.player.y - 1][self.player.x],
                self.maze[self.player.y][self.player.x + 1],
                self.maze[self.player.y + 1][self.player.x],
                self.maze[self.player.y][self.player.x - 1]
            ])

class Player:
    solutionPath = queue.Queue()
    def __init__(self, x=1, y =1):
        self.x = x
        self.y = y
        self.history = []
        self.lastMove = 0
        self.path = None

    def display_player(self):
        return 'P'


    def move(self, directions):
        '''
            params:
                directions: array of characters that represents the objects that
                    are directly N, E, S, W of the player.
        '''
        counter = 0
        while(counter < 4):
            temp_int = self.lastMove + 1 - counter
            if(temp_int < 0):
                temp_int += 4
            if(temp_int > 3):
                temp_int -= 4
            if(directions[temp_int] != "1"):
                self.go_forward(temp_int)
                break
            else:
                counter += 1


    def go_forward(self, direction):
        if direction == Compass["North"]:
            self.y -= 1
            self.history.append("N")
            self.lastMove = Compass["North"]
        elif direction == Compass["East"]:
            self.x += 1
            self.history.append("E")
            self.lastMove = Compass["East"]
        elif direction == Compass["South"]:
            self.y += 1
            self.history.append("S")
            self.lastMove = Compass["South"]
        elif direction == Compass["West"]:
            self.x -= 1
            self.history.append("W")
            self.lastMove = Compass["West"]

    def bad_solve(self, directions):
        north = directions[0]
        east = directions[1]
        south = directions[2]
        west = directions[3]
        if directions.count('E') != 0:
            index = directions.index('E')
            if index == 0:
                self.y -= 1
                self.history.append("N")
            elif index == 1:
                self.x += 1
                self.history.append("E")
            elif index == 2:
                self.y += 1
                self.history.append("S")
            elif index == 3:
                self.x -= 1
                self.history.append("W")
        else:
            if north == ' ' and top(self.history) != "S":
                self.y -= 1
                self.history.append("N")
            elif east == ' ' and top(self.history) != "W":
                self.x += 1
                self.history.append("E")
            elif south == ' ' and top(self.history) != "N":
                self.y += 1
                self.history.append("S")
            elif west == ' ' and top(self.history) != "E":
                self.x -= 1
                self.history.append("W")
            else:
                if top(self.history) == "N":
                    self.y += 1
                    self.history.append("S")
                elif top(self.history) == "E":
                    self.x -= 1
                    self.history.append("W")
                elif top(self.history) == "S":
                    self.y -= 1
                    self.history.append("N")
                elif top(self.history) == "W":
                    self.x += 1
                    self.history.append("E")

    def bfs(self, directions):
        if self.path is None:
            self.path = list(BFS().solution_moves)
        move = self.path.pop(0)
        if move == 'N':
            self.y -= 1
            self.history.append("N")
        elif move == 'E':
            self.x += 1
            self.history.append("E")
        elif move == 'S':
            self.y += 1
            self.history.append("S")
        elif move == 'W':
            self.x -= 1
            self.history.append("W")


class BFS:
    def __init__(self):
        self.player = Player()
        self.maze = to_matrix(Maze().maze)
        self.solution_moves = None
        self.find_path()

    def find_path(self):
        nums = queue.Queue()
        nums.put("")
        add = ""
        the_maze = self.maze
        while not self.is_end(the_maze, add):
            add = nums.get()
            for j in ["N", "E", "S", "W"]:
                put = add + j
                if self.is_valid(the_maze, put):
                    nums.put(put)

    def is_valid(self, maze, moves):
        i, j = self.get_location(maze, moves)
        if not (0 <= i < len(maze[0]) and 0 <= j < len(maze)):
            return False
        elif maze[j][i] == "1":
            return False
        return True

    def is_end(self, maze, moves):
        i, j = self.get_location(maze, moves)
        if maze[j][i] == "E":
            print("Found: " + moves)
            self.solution_moves = list(moves)
            return True
        return False

    def get_location(self, maze, moves):
        i = self.player.x
        j = self.player.y
        for move in moves:
            if move == "W":
                i -= 1
            elif move == "E":
                i += 1
            elif move == "N":
                j -= 1
            elif move == "S":
                j += 1
        return i, j

def main():
    maze = Maze()
    maze.print_maze()
    while maze.is_running:
        maze.update()
        maze.print_maze()
        time.sleep(0.1)


def top(data_list):
    if len(data_list) != 0:
        return data_list[len(data_list) - 1]
    else:
        return None


if __name__ == "__main__":
    main()


# Writing The Spec
# 1. Pick out all of the methods you want them to implement
# 2. Pick out key concepts to focus on (probably logic)
# 3. Help them understand how powerful references can be; using words/Constants
#    to label integers
# 4. Write out spec first and then ponder what knowledge is required to write
#    it out.
#
#
#
