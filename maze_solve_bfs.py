import queue


class MazeBFS:

    def __init__(self, new_maze, start_pos):
        # maze (grid)
        self.maze = new_maze
        # to track algorithm path to exit cell (to find shortest path later)
        self.path = {}
        self.visited_cells_path = []
        # starting point cell
        self.starting_point = [0, start_pos]
        # queue for BFS algorithm (FIFO)
        self.steps_queue = queue.Queue()

    def get_next_cells(self, cell):
        # get neighbouring cells of current cell
        if self.maze[cell[0]][cell[1] - 1] != "w" and self.maze[cell[0]][cell[1] - 1] != "v":
            # enqueue neighbouring valid cell to the queue
            self.steps_queue.put([cell[0], cell[1] - 1])
            # record neighbouring cell parent cell for path reconstruction
            self.path[(cell[0], cell[1] - 1)] = (cell[0], cell[1])
        if self.maze[cell[0]][cell[1] + 1] != "w" and self.maze[cell[0]][cell[1] + 1] != "v":
            self.steps_queue.put([cell[0], cell[1] + 1])
            self.path[(cell[0], cell[1] + 1)] = (cell[0], cell[1])
        if self.maze[cell[0] - 1][cell[1]] != "w" and self.maze[cell[0] - 1][cell[1]] != "v":
            self.steps_queue.put([cell[0] - 1, cell[1]])
            self.path[(cell[0] - 1, cell[1])] = (cell[0], cell[1])
        if self.maze[cell[0] + 1][cell[1]] != "w" and self.maze[cell[0] + 1][cell[1]] != "v":
            self.steps_queue.put([cell[0] + 1, cell[1]])
            self.path[(cell[0] + 1, cell[1])] = (cell[0], cell[1])

    def search(self):
        # Main function for maze search (BFS algorithm)
        # mark starting point as already visited, to avoid extra IndexError checks
        self.maze[0][self.starting_point[1]] = "v"
        # record first parent node
        self.path[(1, self.starting_point[1])] = (self.starting_point[0], self.starting_point[1])
        # enqueue row and column one below starting point as it is always the next move
        self.steps_queue.put([1, self.starting_point[1]])
        # while queue is not empty
        while not self.steps_queue.empty():
            # get first cell from the queue
            current_cell = self.steps_queue.get()
            # when exit found, clear queue to stop BFS as shortest path can be generated
            if self.maze[current_cell[0]][current_cell[1]] == "e":
                # if exit cell is found, return exit cell
                return current_cell[0], current_cell[1]
            else:
                # mark cell as visited
                self.maze[current_cell[0]][current_cell[1]] = "v"
                self.visited_cells_path.append([current_cell[0], current_cell[1]])
                # get neighbouring valid cells
                self.get_next_cells(current_cell)

    def reconstruct_path(self, cell):
        # Shortest path reconstruction
        # initialise final path list and add exit node to it
        final_path = [cell]
        # while parent nodes can be found, go through cells
        while True:
            if cell in self.path:
                final_path.append(self.path[cell])
                cell = self.path[cell]
            else:
                # return final path when iteration between exit node and start node is found
                return final_path

    def maze_solve(self):
        row, col = self.search()
        exit_cell = (row, col)
        new_path = self.reconstruct_path(exit_cell)
        # convert tuples inside list to lists inside list
        new_path = [list(path) for path in new_path]
        return new_path
