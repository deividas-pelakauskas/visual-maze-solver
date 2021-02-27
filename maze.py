import random


class Maze:

    cell = "c"  # cell marking on maze
    unv_cell = "u"  # unvisited cell marking on maze
    wall = "w"  # wall marking on maze

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = [[self.unv_cell for i in range(self.width)] for j in range(self.height)]
        self.walls = []
        self.path = []  # to record path how maze is generated for visualisation later
        self.start_pos = 0  # starting coordinate for maze
        self.exit_pos = 0  # exit coordinate for maze

    def generate_full_maze(self):
        # Generates full maze including start and exit positions
        self.starting_position()  # set starting position and walls around it
        self.generate_maze()  # generates walls and passages
        self.remaining_walls()  # marks remaining unvisited cells as walls
        self.set_entrance_exit() # set entrance point for the maze

    def generate_maze(self):
        # Main function that generates maze
        while self.walls:
            # select random wall from existing walls
            random_wall = self.walls[(random.randint(0, len(self.walls) - 1))]

            if random_wall[1] != 0:  # check if it is not the first column on the left
                # check if on the left next to the generated previously random wall there as an unvisited cell
                # check if there is a cell next to random wall on the right
                if self.maze[random_wall[0]][random_wall[1] - 1] == self.unv_cell and self.maze[random_wall[0]][random_wall[1] + 1] == self.cell:
                    if self.surrounding_cell_count(random_wall) < 2:  # get number of surrounding cells
                        # turn wall into passage if there are less than two surround cells
                        self.maze[random_wall[0]][random_wall[1]] = self.cell
                        # record new cell for visualisation
                        self.path.append(random_wall)
                        # mark surrounding walls as part of maze
                        # mark upper, bottom and left walls, because there is a cell on the right
                        self.mark_upper_wall(random_wall)
                        self.mark_bottom_wall(random_wall)
                        self.mark_left_wall(random_wall)
                        # remove processed wall from the walls list and continue to next iteration
                        self.delete_wall(random_wall)
                        continue

            if random_wall[0] != 0:  # check if it is not the first row of the maze
                if self.maze[random_wall[0] - 1][random_wall[1]] == self.unv_cell and self.maze[random_wall[0] + 1][random_wall[1]] == self.cell:
                    if self.surrounding_cell_count(random_wall) < 2:
                        self.maze[random_wall[0]][random_wall[1]] = self.cell
                        self.path.append(random_wall)
                        self.mark_upper_wall(random_wall)
                        self.mark_left_wall(random_wall)
                        self.mark_right_wall(random_wall)
                        self.delete_wall(random_wall)
                        continue

            if random_wall[0] != self.height - 1:  # check if it is not a last row of the maze
                if self.maze[random_wall[0] + 1][random_wall[1]] == self.unv_cell and self.maze[random_wall[0] - 1][random_wall[1]] == self.cell:
                    if self.surrounding_cell_count(random_wall) < 2:
                        self.maze[random_wall[0]][random_wall[1]] = self.cell
                        self.path.append(random_wall)
                        self.mark_bottom_wall(random_wall)
                        self.mark_left_wall(random_wall)
                        self.mark_right_wall(random_wall)
                        self.delete_wall(random_wall)
                        continue

            if random_wall[1] != self.width - 1:  # check if it is not the last column of the maze
                if self.maze[random_wall[0]][random_wall[1] + 1] == self.unv_cell and self.maze[random_wall[0]][random_wall[1] - 1] == self.cell:
                    if self.surrounding_cell_count(random_wall) < 2:
                        self.maze[random_wall[0]][random_wall[1]] = self.cell
                        self.path.append(random_wall)
                        self.mark_right_wall(random_wall)
                        self.mark_bottom_wall(random_wall)
                        self.mark_upper_wall(random_wall)
                        self.delete_wall(random_wall)
                        continue

            # if none of the conditions are met, delete wall from the list anyway
            for wall in self.walls:
                if wall[0] == random_wall[0] and wall[1] == random_wall[1]:
                    self.walls.remove(wall)

    def starting_position(self):
        # Pick random starting position and mark walls around it

        first_row = random.randint(0, self.height - 1)  # starting position (coordinate) in a row
        first_col = random.randint(0, self.width - 1)  # starting position (coordinate) in a column

        # Make sure that starting position is not on the edge of the maze
        if first_row == 0:
            first_row = 1

        if first_row == self.height - 1:
            first_row -= 1

        if first_col == 0:
            first_col = 1

        if first_col == self.width - 1:
            first_col -= 1

        # Mark starting position as a cell
        self.maze[first_row][first_col] = self.cell
        self.path.append(list([first_row, first_col]))

        # Mark walls around starting cell in the grid
        self.maze[first_row - 1][first_col] = self.wall
        self.maze[first_row + 1][first_col] = self.wall
        self.maze[first_row][first_col - 1] = self.wall
        self.maze[first_row][first_col + 1] = self.wall

        # Add walls around starting cell to the walls list
        self.walls.append([first_row - 1, first_col])
        self.walls.append([first_row + 1, first_col])
        self.walls.append([first_row, first_col - 1])
        self.walls.append([first_row, first_col + 1])

    def surrounding_cell_count(self, wall):
        # Count how many cells around given wall there is
        # this is used to make sure that every attempt to make a passage does not have more than one cell around it
        cell_count = 0
        if self.maze[wall[0] - 1][wall[1]] == self.cell:
            cell_count += 1
        if self.maze[wall[0] + 1][wall[1]] == self.cell:
            cell_count += 1
        if self.maze[wall[0]][wall[1] - 1] == self.cell:
            cell_count += 1
        if self.maze[wall[0]][wall[1] + 1] == self.cell:
            cell_count += 1
        return cell_count

    def mark_upper_wall(self, wall):
        # Mark as wall above cell after another wall was turned into a passage
        if wall[0] != 0:
            if self.maze[wall[0] - 1][wall[1]] != self.cell:
                self.maze[wall[0] - 1][wall[1]] = self.wall
            if [wall[0] - 1, wall[1]] not in self.walls:
                self.walls.append([wall[0] - 1, wall[1]])

    def mark_bottom_wall(self, wall):
        # Mark as wall below cell after another wall was turned into a passage
        if wall[0] != self.height - 1:
            if self.maze[wall[0] + 1][wall[1]] != self.cell:
                self.maze[wall[0] + 1][wall[1]] = self.wall
            if [wall[0] + 1, wall[1]] not in self.walls:
                self.walls.append([wall[0] + 1, wall[1]])

    def mark_left_wall(self, wall):
        # Mark as wall left to cell after another wall was turned into a passage
        if wall[1] != 0:
            if self.maze[wall[0]][wall[1] - 1] != self.cell:
                self.maze[wall[0]][wall[1] - 1] = self.wall
            if [wall[0], wall[1] - 1] not in self.walls:
                self.walls.append([wall[0], wall[1] - 1])

    def mark_right_wall(self, wall):
        # Mark as wall right to cell after another wall was turned into a passage
        if wall[1] != self.width - 1:
            if self.maze[wall[0]][wall[1] + 1] != self.cell:
                self.maze[wall[0]][wall[1] + 1] = self.wall
            if [wall[0], wall[1] + 1] not in self.walls:
                self.walls.append([wall[0], wall[1] + 1])

    def delete_wall(self, random_wall):
        # Delete random wall from the list if it is in the list
        for wall in self.walls:
            if wall[0] == random_wall[0] and wall[1] == random_wall[1]:
                self.walls.remove(wall)

    def remaining_walls(self):
        # Function marks remaining unvisited cells as walls
        for row in range(self.height):
            for col in range(self.width):
                if self.maze[row][col] == self.unv_cell:
                    self.maze[row][col] = self.wall

    def set_entrance_exit(self):
        # Sets starting point and exit point on the maze and saves starting point for solving algorithm

        # get second row indexes where cells are located
        entrance_indexes = [index for index in range(len(self.maze[1])) if self.maze[1][index] == "c"]
        # get one before last row indexes where cells are located
        exit_indexes = [index for index in range(len(self.maze[self.height - 2])) if self.maze[self.height - 2][index] == "c"]
        # select random index for entrance point
        random_entrance = random.choice(entrance_indexes)
        # select random index for exit point
        random_exit = random.choice(exit_indexes)
        # mark starting point
        self.maze[0][random_entrance] = "s"
        # mark exit point
        self.maze[self.height - 1][random_exit] = "e"
        # record starting point for solving algorithms
        self.start_pos = random_entrance
        self.exit_pos = random_exit
        self.path.append([0, random_entrance])
        self.path.append([len(self.maze) - 1, random_exit])