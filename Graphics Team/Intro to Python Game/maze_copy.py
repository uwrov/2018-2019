import os
import time
import queue


def createMaze2():
    maze = []
    maze.append(["#", "#", "#", "#", "#", "O", "#", "#", "#"])
    maze.append(["#", " ", " ", " ", " ", " ", " ", " ", "#"])
    maze.append(["#", " ", "#", "#", " ", "#", "#", " ", "#"])
    maze.append(["#", " ", "#", " ", " ", " ", "#", " ", "#"])
    maze.append(["#", " ", "#", " ", "#", " ", "#", " ", "#"])
    maze.append(["#", " ", "#", " ", "#", " ", "#", " ", "#"])
    maze.append(["#", " ", "#", " ", "#", " ", "#", "#", "#"])
    maze.append(["#", " ", " ", " ", " ", " ", " ", " ", "#"])
    maze.append(["#", "#", "#", "#", "#", "#", "#", "E", "#"])
    return maze


def to_matrix(maze):
    matrix = []
    for s in maze:
        matrix.append(list(s))
    return matrix


class Maze:
    def __init__(self):
        # self.maze = [['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
        #              ['1', ' ', '1', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1'],
        #              ['1', ' ', '1', '1', '1', ' ', '1', '1', '1', '1', '1'],
        #              ['1', '1', '1', '1', '1', '1','1','1','1','1'],
        #             ['1',  '1', '1', '1', '1','1','1','1','1'],
        #              ['1','1', '1', '1', '1', '1','1','1','1','1'],
        #              ['1',  '1', '1', '1', '1','1','1','1','1'],
        #              ['1','1',   '1', '1',    '1','1'],
        #              ['1',  '1', '1','1','1','1','1','1',  '1'],
        #              ['1','1', '1',     '1','1','1', '1'],
        #              ['1','1','1',  '1','1','1',   '1','E','1'],
        #              ['1','1','1','1','1','1','1','1','1','1','1','1','1','1']]
        self.maze = createMaze2()
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
    def __init__(self, x=1, y=1):
        self.x = x
        self.y = y
        self.history = []
        self.lastMove = 0
        self.solution_moves = None
        self.find_path()

    def display_player(self):
        return 'P'

    def find_path(self):
        nums = queue.Queue()
        nums.put("")
        add = ""
        maze = createMaze2()
        while not self.is_end(maze, add):
            add = nums.get()
            for j in ["N", "E", "S", "W"]:
                put = add + j
                if self.is_valid(maze, put):
                    nums.put(put)

    def bfs(self, directions):
        move = self.solution_moves.pop(0)
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

    def is_valid(self, maze, moves):
        i, j = self.get_location(maze, moves)
        if not (0 <= i < len(maze[0]) and 0 <= j < len(maze)):
            return False
        elif maze[j][i] == "#":
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
        i = self.x
        j = self.y
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
