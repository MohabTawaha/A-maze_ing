*This activity has been created as part of the 42 curriculum by wal-deek, mal-tawa.*

# A-Maze-ing

## Description

A-Maze-ing is a Python program that generates and displays mazes from a configuration file. It supports reproducible generation using a seed, finds a shortest path between entry and exit, and saves the result using hexadecimal wall values.

Two modes are available:

- **Perfect mode:** a connected maze without loops.
- **Non-perfect mode:** a connected board with multiple routes and few dead ends, suitable for a Pac-Man-like game.

The maze includes a visible “42” pattern when its dimensions allow it. The terminal display uses swords for the entry, a diamond for the exit, and colored dots for the solution.

Users can regenerate the maze, show or hide its shortest path, change colors, and quit.

## Instructions

### Requirements

- Python 3.10 or newer.
- A terminal supporting ANSI colors and Unicode.

### Installation and execution

```sh
make install
make run
```

To run with a specific configuration file:

```sh
python3 a_maze_ing.py config.txt
```

### Development commands

| Command        | Purpose                                 |
| -------------- | --------------------------------------- |
| `make install` | Install dependencies                    |
| `make run`     | Run the program                         |
| `make debug`   | Run through Python’s debugger           |
| `make clean`   | Remove temporary files and caches       |
| `make lint`    | Run flake8 and the required mypy checks |

### Configuration

The configuration contains one `KEY=VALUE` pair per line. Blank lines and lines starting with `#` are ignored.

| Key           | Required | Meaning                                  |
| ------------- | -------- | ---------------------------------------- |
| `WIDTH`       | Yes      | Positive number of columns               |
| `HEIGHT`      | Yes      | Positive number of rows                  |
| `ENTRY`       | Yes      | Entry coordinates in `x,y` format        |
| `EXIT`        | Yes      | Exit coordinates in `x,y` format         |
| `OUTPUT_FILE` | Yes      | Destination file path                    |
| `PERFECT`     | Yes      | `True` or `False`                        |
| `SEED`        | No       | Integer used for reproducible generation |

Example:

```text
WIDTH=15
HEIGHT=15
ENTRY=0,0
EXIT=14,14
OUTPUT_FILE=my_maze.txt
PERFECT=True
SEED=42
```

Coordinates start at `(0,0)` in the top-left corner. Entry and exit must be different, inside the maze, and outside the “42” pattern.

Single-row, single-column, and 2×2 boards are rejected in non-perfect mode because they cannot provide two independent loops. Boolean values are case-sensitive.

A default `config.txt` is included in the repository. With the same seed and generation settings, the maze is reproducible.

### Controls

| Choice | Action                             |
| ------ | ---------------------------------- |
| `1`    | Regenerate and display the maze    |
| `2`    | Show or hide the shortest path     |
| `3`    | Cycle wall and “42” pattern colors |
| `4`    | Quit                               |

Regeneration hides the new solution while preserving the selected colors. Ctrl+C and end-of-input exit gracefully.

### Output format

Each maze cell is represented by one hexadecimal digit. A set bit indicates a closed wall.

| Bit | Direction |
| --- | --------- |
| 0   | North     |
| 1   | East      |
| 2   | South     |
| 3   | West      |

Maze rows are followed by an empty line, entry coordinates, exit coordinates, and the shortest path using `N`, `E`, `S`, and `W`. Every line ends with a newline.

## Algorithm

Maze generation uses **randomized depth-first search**, also known as the backtracking algorithm. Non-perfect mode adds passages to provide alternative routes and reduce dead ends.

We chose this algorithm because it is straightforward to understand, produces winding mazes, and supports reproducible generation.

The shortest path is found using **breadth-first search (BFS)** because every move has the same cost.

## Reusable Generator

`MazeGenerator` is the reusable part of the project. It provides maze generation, access to the maze structure, and access to a solution independently of the terminal display.

An installable `mazegen-*` distribution is provided at the repository root, together with its documentation and build sources.

Install the supplied package by passing its exact filename to:

```sh
python3 -m pip install <package-file>
```

Rebuild it from the project root with:

```sh
python3 -m build
```

### Basic usage

The following example uses the source modules from the repository:

```python
from config_parser import MazeConfig
from maze_generator import MazeGenerator

config = MazeConfig(
    width=10,
    height=10,
    entry=(0, 0),
    exit=(9, 9),
    output_file="maze.txt",
    perfect=True,
    seed=42,
)

generator = MazeGenerator(config, set())
generator.generate()

maze = generator.grid
solution = generator.find_shortest_path()
directions = generator.get_path_directions()
```

Custom dimensions, entry, exit, mode, and seed are supplied through `MazeConfig`. The second constructor argument contains blocked coordinates; an empty set means no blocked cells.

- `grid` provides the generated structure.
- `find_shortest_path()` returns the solution coordinates.
- `get_path_directions()` returns the solution as direction letters.

Use valid parameters and a fresh generator instance for each new maze. Package documentation describes its installed imports and usage.

## Team and Project Management

### Contributions

| Member     | Main responsibilities                                                              |
| ---------- | ---------------------------------------------------------------------------------- |
| mal-tawa   | Configuration parsing, maze generation, shortest-path search, and output format    |
| wal-deek   | Terminal display, menu interactions, colors, entry/exit markers, and documentation |
| Both       | Design decisions, testing, error handling, packaging, and final review             |

### Planning and changes

Our initial plan was to understand the maze requirements, build the core generator, add the display, and finish with testing and delivery.

During development, we divided the interactive features into smaller steps. Regeneration, path visibility, color changes, and entry/exit markers were implemented and checked separately. Additional time was dedicated to invalid board sizes and terminal input handling.

### What worked well

Working in small steps made the code easier to understand and problems easier to locate. Testing each menu action separately helped us check that the displayed maze and program state stayed consistent.

### What could improve

Earlier automated testing and documentation would reduce the amount of work needed at the end. More testing across different sizes and seeds would also help identify generation problems sooner.

### Tools

We used Python, a terminal, flake8, mypy, Python’s debugger, Python build tools, and ChatGPT for learning support and review.

## Resources

- [Python documentation](https://docs.python.org/3/)
- [Python random module](https://docs.python.org/3/library/random.html)
- [Python collections module](https://docs.python.org/3/library/collections.html)
- [PEP 257 — Docstring conventions](https://peps.python.org/pep-0257/)
- [Flake8 documentation](https://flake8.pycqa.org/en/latest/)
- [Mypy documentation](https://mypy.readthedocs.io/en/stable/)
- [Python packaging guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Graph traversal: DFS and BFS](https://algs4.cs.princeton.edu/41graph/)
- The A-Maze-ing subject for project requirements.

### AI use

ChatGPT supported explanations of maze concepts, reviews of code snippets, suggestions for small development steps, terminal styling ideas, and test scenarios. It also assisted with a project review and drafting this README.

Its assistance covered configuration handling, generation, shortest paths, regeneration state, display conditions, colors, and error handling. The team reviewed suggestions and tested changes rather than treating AI output as proof of correctness.

## License

The reuse and distribution terms for the generator are provided in the root-level `LICENSE.md`.
