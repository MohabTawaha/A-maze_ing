import sys

from config_parser import parse_config, read_config_file
from maze_generator import MazeGenerator
from pattern_42 import get_pattern_cells
from maze_printer import maze_printer
from maze_writer import write_maze
from maze_colors import wall_color, blocked_cells_colors


def read_config_and_generate(config_filepath: str) -> MazeGenerator:
    """
        Purpose: Read maze settings, prepare the “42” pattern, and generate a
        maze.
        Args: config_filepath — path to the configuration file.
        Returns: A MazeGenerator object containing the generated maze.
        Raises:
        - ValueError — invalid configuration or entry/exit inside the “42”
        pattern.
        - OSError — the configuration file cannot be opened or read.
    """
    maze_dict = read_config_file(config_filepath)
    maze_obj = parse_config(maze_dict)
    myset = get_pattern_cells(maze_obj.width, maze_obj.height)
    if maze_obj.entry in myset:
        raise ValueError("Entry cell cannot be part of 42 pattern")
    if maze_obj.exit in myset:
        raise ValueError("Exit cell cannot be part of 42 pattern")
    if len(myset) == 0:
        print("Maze is too small for the 42 pattern, generating without it")

    maze_gen_obj = MazeGenerator(maze_obj, myset)
    maze_gen_obj.generate()

    return maze_gen_obj


def main() -> None:
    """
        Purpose: Generate, display, and save a maze, then handle the
        interactive menu.
        Args: None. The configuration path comes from command-line arguments
        through sys.argv.
        Returns: None.
        Error handling: Explain that configuration and file errors are
        displayed, and Ctrl+C or end-of-input exits gracefully.
    """
    if len(sys.argv) != 2:
        print("expected one config file path")
        print("Usage: python3 a_maze_ing.py <config_file>")
        return
    try:
        filename: str = sys.argv[1]
        maze_obj = read_config_and_generate(filename)
        show_path: bool = False
        path_cells: set[tuple[int, int]] = set(maze_obj.find_shortest_path())
        color_idx: int = 0
        maze_printer(maze_obj.grid, maze_obj.blocked_cells,
                     path_cells, show_path, wall_color[color_idx],
                     blocked_cells_colors[color_idx],
                     maze_obj.config.entry, maze_obj.config.exit)
        write_maze(maze_obj.config.output_file, maze_obj.grid,
                   maze_obj.config.entry,
                   maze_obj.config.exit, maze_obj.get_path_directions())

        while (True):
            print("===A-Maze-ing===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide the shortest path from entry and exit")
            print("3. Rotate maze colors")
            print("4. Quit")
            user_choice = input("Choice? (1-4) ")
            user_choice = user_choice.strip()
            if user_choice == "4":
                break
            elif user_choice == "1":
                try:
                    new_maze = read_config_and_generate(filename)
                    write_maze(new_maze.config.output_file, new_maze.grid,
                               new_maze.config.entry, new_maze.config.exit,
                               new_maze.get_path_directions())
                    maze_obj = new_maze
                    show_path = False
                    path_cells = set(maze_obj.find_shortest_path())
                    maze_printer(maze_obj.grid, maze_obj.blocked_cells,
                                 path_cells, show_path, wall_color[color_idx],
                                 blocked_cells_colors[color_idx],
                                 maze_obj.config.entry, maze_obj.config.exit)

                except ValueError as error:
                    print(error)
                except OSError as error:
                    print(error)
            elif user_choice == "2":
                show_path = not show_path
                maze_printer(maze_obj.grid, maze_obj.blocked_cells,
                             path_cells, show_path, wall_color[color_idx],
                             blocked_cells_colors[color_idx],
                             maze_obj.config.entry, maze_obj.config.exit)
            elif user_choice == "3":
                color_idx += 1
                if color_idx == len(wall_color):
                    color_idx = 0
                maze_printer(maze_obj.grid, maze_obj.blocked_cells,
                             path_cells, show_path, wall_color[color_idx],
                             blocked_cells_colors[color_idx],
                             maze_obj.config.entry, maze_obj.config.exit)

    except ValueError as error:
        print(error)
    except OSError as error:
        print(error)
    except EOFError as error:
        print(error)
    except KeyboardInterrupt as error:
        print(error)


if __name__ == "__main__":
    main()
