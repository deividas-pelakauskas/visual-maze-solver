import heapq


class Cell:

    def __init__(self, row, col, weight=0):
        self.row = row
        self.col = col
        self.weight = weight

    # for comparison in priority queue
    def __lt__(self, other):
        return self.weight < other.weight


class MazeDijkstra:

    def __init__(self, new_maze, start_pos, maze_height, exit_pos):
        # maze (grid)
        self.maze = new_maze
        # starting point cell
        self.starting_point = [0, start_pos]
        self.exit_point = [maze_height - 1, exit_pos]
        self.path = {}
        # to record already visited cells to make sure that same cell is not added to the queue
        self.visited_cells = []

    def get_cell_weight(self, cell):
        # get cell weight
        row = cell[0]
        col = cell[1]
        weight = abs(row - self.exit_point[0]) + abs(col - self.exit_point[1])
        return weight

    def get_next_cells(self, cell):
        # get neighbouring cells of current cell
        cells = []
        if self.maze[cell[0]][cell[1] - 1] != "w" and self.maze[cell[0]][cell[1] - 1] != "v":
            cells.append([cell[0], cell[1] - 1])
        if self.maze[cell[0]][cell[1] + 1] != "w" and self.maze[cell[0]][cell[1] + 1] != "v":
            cells.append([cell[0], cell[1] + 1])
        if self.maze[cell[0] - 1][cell[1]] != "w" and self.maze[cell[0] - 1][cell[1]] != "v":
            cells.append([cell[0] - 1, cell[1]])
        if self.maze[cell[0] + 1][cell[1]] != "w" and self.maze[cell[0] + 1][cell[1]] != "v":
            cells.append([cell[0] + 1, cell[1]])
        return cells

    def search(self):
        # Main function for maze search (Dijkstra's algorithm)
        # mark starting point as already visited, to avoid extra IndexError checks
        self.maze[0][self.starting_point[1]] = "v"
        # record first cell
        self.visited_cells = [[0, self.starting_point[1]]]
        # record first cell in path (starting point)
        self.path[(1, self.starting_point[1])] = (self.starting_point[0], self.starting_point[1])
        # record first parent cell
        start_cell = Cell(1, self.starting_point[1], self.get_cell_weight([1, self.starting_point[1]]))
        # add first cell object to queue
        queue = [start_cell]
        heapq.heapify(queue)
        # while queue is not empty
        while queue:
            # get next cell from queue
            current_cell = heapq.heappop(queue)
            self.visited_cells.append([current_cell.row, current_cell.col])
            # when exit found, finish loop and return exit cell
            if self.maze[current_cell.row][current_cell.col] == "e":
                return current_cell.row, current_cell.col
            else:
                # mark cell as visited
                self.maze[current_cell.row][current_cell.col] = "v"
                # get neighbouring valid cells
                next_cells = self.get_next_cells([current_cell.row, current_cell.col])
                # check all neighbouring cells of current cell
                for next_cell in next_cells:
                    # if next cell in neighbouring cells is not already visited and not already in the queue
                    # initialise new cell object and add it to the queue
                    if next_cell not in self.visited_cells and not any(
                            cell.row == next_cell[0] and cell.col == next_cell[1] for cell in queue):
                        new_cell = Cell(next_cell[0], next_cell[1], self.get_cell_weight(next_cell))
                        heapq.heappush(queue, new_cell)
                        self.path[(next_cell[0], next_cell[1])] = (current_cell.row, current_cell.col)

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
