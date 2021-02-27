from flask import Flask, render_template, request
import copy
import maze
import maze_solve_bfs
import maze_solve_dfs
import maze_solve_dijkstra

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def generate_maze():
    # Generate maze
    # if user selected maze size, then make mize of the selected size, otherwise create the small one (15 x 15)
    try:
        maze_size = request.form.get("maze-size")
        if maze_size == "1":
            new_maze = maze.Maze(15, 15)
        elif maze_size == "2":
            new_maze = maze.Maze(20, 20)
        elif maze_size == "3":
            new_maze = maze.Maze(30, 30)
        elif maze_size == "4":
            new_maze = maze.Maze(60, 30)
        else:
            new_maze = maze.Maze(15, 15)
    except:
        new_maze = maze.Maze(15, 15)

    # generate maze
    new_maze.generate_full_maze()
    # get full generate maze with walls, cells, starting point and exit point
    full_maze = new_maze.maze
    # get path on how maze was generated using Prim's algorithm
    maze_path = new_maze.path
    # solve maze using BFS algorithm
    maze_bfs, maze_bfs_shortest_path = solve_maze_bfs(copy.deepcopy(full_maze), new_maze.start_pos)
    # solve maze using DFS algorithm
    maze_dfs, maze_dfs_path = solve_maze_dfs(copy.deepcopy(full_maze), new_maze.start_pos)
    # solve maze using Dijkstra's algorithm
    maze_dijkstra, maze_dijkstra_path = solve_maze_dijkstra(copy.deepcopy(full_maze), new_maze.start_pos,
                                                            new_maze.height, new_maze.exit_pos)
    return render_template("maze.html", maze_grid=full_maze, maze_path=maze_path, maze_size=maze_size,
                           maze_bfs_path=maze_bfs, maze_bfs_shortest_path=maze_bfs_shortest_path,
                           maze_dfs_path=maze_dfs, maze_dfs_final_path=maze_dfs_path,
                           maze_dijkstra_path=maze_dijkstra, maze_dijkstra_shortest_path=maze_dijkstra_path)


def solve_maze_bfs(new_maze, start_pos):
    # Solve maze using BFS
    maze_solve = maze_solve_bfs.MazeBFS(new_maze, start_pos)
    shortest_path = maze_solve.maze_solve()
    return maze_solve.visited_cells_path, shortest_path


def solve_maze_dfs(new_maze, start_pos):
    # Solve maze using DFS (recursion)
    maze_solve = maze_solve_dfs.MazeDFS(new_maze)
    maze_solve.search(0, start_pos)
    return maze_solve.path, maze_solve.final_path


def solve_maze_dijkstra(new_maze, start_pos, maze_height, exit_pos):
    # Solve maze using Dijkstra's algorithm
    maze_solve = maze_solve_dijkstra.MazeDijkstra(new_maze, start_pos, maze_height, exit_pos)
    shortest_path = maze_solve.maze_solve()
    return maze_solve.visited_cells, shortest_path


if __name__ == '__main__':
    app.run()
