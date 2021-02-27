class MazeDFS:

    def __init__(self, maze):
        self.maze = maze
        self.path = []  # to track steps that were taken to solve maze
        self.final_path = []  # track final path

    def search(self, row, col):
        if self.maze[row][col] == "e":
            return True
        elif self.maze[row][col] == "w":
            return False
        elif self.maze[row][col] == "v":
            return False

        self.maze[row][col] = "v"
        self.path.append([row, col])

        # check neighbouring paths clockwise by starting on the right one
        if (col < len(self.maze[0]) - 1 and self.search(row, col + 1)) \
                or (row < len(self.maze[0]) and self.search(row + 1, col)) \
                or (col > 0 and self.search(row, col - 1)) \
                or (row > 0 and self.search(row - 1, col)):
            self.final_path.append([row, col])
            return True
        return False