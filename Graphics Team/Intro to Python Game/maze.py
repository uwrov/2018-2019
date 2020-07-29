import numpy as np
import os
import time
import queue

Compass = {
    "North": 0,
    "East": 1,
    "South": 2,
    "West": 3
}


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

    def update_maze(self):
        if self.is_running:
            for y in range(0, len(self.maze)):
                if self.is_running:
                    for x in range(0, len(self.maze[y])):
                        if self.player.x == x and self.player.y == y:
                            if self.maze[y][x] == "1":
                                self.is_running = False
                                break
                            elif self.maze[y][x] == "E":
                                self.is_running = False
                                break

    def update(self):
        if self.is_running:
            self.player.BFS([
                self.maze[self.player.y - 1][self.player.x],
                self.maze[self.player.y][self.player.x + 1],
                self.maze[self.player.y + 1][self.player.x],
                self.maze[self.player.y][self.player.x - 1]
            ])
    def get_neighbors(self):
        return [self.maze[self.player.y - 1][self.player.x],
                self.maze[self.player.y][self.player.x + 1],
                self.maze[self.player.y + 1][self.player.x],
                self.maze[self.player.y][self.player.x - 1]
               ]



class Player:
    solutionPath = queue.Queue()
    def __init__(self, x=1, y =1):
        self.x = x
        self.y = y
        self.history = []
        self.lastMove = 0
        # solutionPath = self.findPath(Maze().update())

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

    def findPath(self,directions):
        maze = Maze()
        nums = queue.Queue()
        path = queue.Queue()
        path.put("")
        nums.put("")
        add = ""
        add2 = ""
        while maze.is_running:
            add = nums.get()
            print("add"+add)
            add2 = path.get()
            print("add2"+add2)
            count = 0
            for p in directions:
                if p == ' ' or p == 'E':
                    put = add + p
                    put2 = add2 + self.get_direction(count)
                    print("put" + put)
                    print("put2"+put2)
                    nums.put(put)
                    path.put(put)
                    self.get_move(count)
                    maze.get_neighbors()
                    maze.update_maze()
                count += 1
        return path

    def BFS(self, directions):
        global solutionPath
        solutionPath = self.findPath(directions)
        print(solutionPath)
        for p in solutionPath:
            if p == 'N':
                self.y -= 1
                self.history.append("N")
            elif p == Compass["East"]:
                self.x += 1
                self.history.append("E")
            elif p == 'S':
                self.y += 1
                self.history.append("S")
            elif p == 'W':
                self.x -= 1
                self.history.append("W")

    def get_direction(self, count):
        if count == 0:
            return 'N'
        elif count == 1:
            return 'E'
        elif count == 2:
            return 'S'
        else:
            return 'W'
    def get_move(self, count):
        if count == 0:
            self.y -= 1
        elif count == 1:
            self.x += 1
        elif count == 2:
            self.y += 1
        else:
            self.x -= 1

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
