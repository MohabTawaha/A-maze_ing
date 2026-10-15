from maze_generator import EAST, SOUTH


def maze_printer(maze: list[list[int]],
                 blocked_cells: set[tuple[int, int]],
                 path_cells: set[tuple[int, int]], show_path: bool,
                 wall_color: str, blocked_color: str,
                 entry: tuple[int, int],
                 exit: tuple[int, int]) -> None:
    """
        Purpose: Display the maze, blocked cells, entry, exit, and optional
        solution dots in the terminal.
        Args:
        - maze: Rows of maze wall values.
        - blocked_cells: Coordinates forming the blocked pattern.
        - path_cells: Coordinates belonging to the shortest path.
        - show_path: Whether to display solution dots.
        - wall_color: color sequence for walls.
        - blocked_color: background color sequence for blocked cells.
        - Include your entry and exit parameters using their exact names.
        Returns: None.
    """
    height = len(maze)
    width = len(maze[0])

    print(wall_color, end="")
    print("┏", end="")
    for i in range(width):
        if i == width - 1:
            print("━━━┓")
        else:
            print("━━━┳", end="")

    for y in range(height):
        print(wall_color, end="")
        print("┃", end="")
        for x in range(width):
            if (x, y) in blocked_cells:
                print(blocked_color + "   " + wall_color, end="")
            elif (x, y) == entry:
                print("🐰 ", end="")
            elif (x, y) == exit:
                print("🥕 ", end="")
            elif (x, y) in path_cells and show_path:
                print("\033[40;97m ⬤ " + wall_color, end="")
            else:
                print("   ", end="")
            if (maze[y][x] & EAST) != 0:
                print("┃", end="")
            else:
                print(" ", end="")
        print("\033[0m")
        print(wall_color, end="")
        if y == height - 1:
            print("┗", end="")
        else:
            print("┣", end="")
        for x in range(width):
            if (maze[y][x] & SOUTH) != 0:
                print("━━━", end="")
            else:
                print("   ", end="")
            if x == width - 1:
                if y == height - 1:
                    print("┛", end="")
                else:
                    print("┫", end="")
            else:
                if y == height - 1:
                    print("┻", end="")
                else:
                    print("╋", end="")

        print("\033[0m")
