import random
from config_parser import MazeConfig
from collections import deque


NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


class MazeGenerator:
    """
        Purpose: Generate mazes and provide access to their structure and
        shortest path.
        Attributes:
        - config: Maze settings.
        - blocked_cells: Coordinates excluded from generation.
        - grid: Rows of cell values representing closed walls
    """

    def __init__(self, config: MazeConfig,
                 blocked_cells: set[tuple[int, int]]):
        """
            Purpose: Store maze settings and create a grid with all walls
            closed.
            Args:
            - config: Maze configuration object.
            - blocked_cells: Coordinates that must remain blocked.
            Returns: None.
        """

        self.config = config
        self.blocked_cells = blocked_cells
        self.grid = []
        for i in range(config.height):
            row = []
            for j in range(config.width):
                row.append(15)
            self.grid.append(row)

    def open_passage(self, curr_cell: tuple[int, int],
                     neigh_cell: tuple[int, int]) -> None:
        """
            Purpose: Remove the shared wall between two neighboring cells.
            Args:
            - curr_cell: Coordinates of the first cell.
            - neigh_cell: Coordinates of the neighboring cell.
            Returns: None; updates the grid.
        """

        x1, y1 = curr_cell
        x2, y2 = neigh_cell
        if y2 == y1 and x2 - x1 == 1:
            self.grid[y1][x1] = self.grid[y1][x1] & ~EAST
            self.grid[y2][x2] = self.grid[y2][x2] & ~WEST

        if y2 == y1 and x2 - x1 == -1:
            self.grid[y1][x1] = self.grid[y1][x1] & ~WEST
            self.grid[y2][x2] = self.grid[y2][x2] & ~EAST

        if x2 == x1 and y2 - y1 == 1:
            self.grid[y1][x1] = self.grid[y1][x1] & ~SOUTH
            self.grid[y2][x2] = self.grid[y2][x2] & ~NORTH

        if x2 == x1 and y2 - y1 == -1:
            self.grid[y1][x1] = self.grid[y1][x1] & ~NORTH
            self.grid[y2][x2] = self.grid[y2][x2] & ~SOUTH

    def get_neighbors(self,
                      coordinate: tuple[int, int]) -> list[tuple[int, int]]:
        """
            Purpose: Find neighboring cells inside the maze, regardless
            of walls.
            Args: coordinate — coordinates of the cell.
            Returns: A list of neighboring coordinates.
        """

        x, y = coordinate
        neighbors: list[tuple[int, int]] = []
        if y > 0:
            neighbors.append((x, y - 1))

        if x < self.config.width - 1:
            neighbors.append((x + 1, y))

        if y < self.config.height - 1:
            neighbors.append((x, y + 1))

        if x > 0:
            neighbors.append((x - 1, y))

        return neighbors

    def generate(self) -> None:
        """
            Purpose: Generate a maze using randomized depth-first search (DFS)
            and reduce dead ends in non-perfect mode.
            Args: None.
            Returns: None; updates the grid.
        """

        visited_cells: set[tuple[int, int]] = {self.config.entry}
        stack: list[tuple[int, int]] = [self.config.entry]
        rand = random.Random(self.config.seed)
        while (len(stack) > 0):
            current_cell = stack[-1]
            neighbors = self.get_neighbors(current_cell)
            unvisited_neighbors = []

            for n in neighbors:
                if n not in visited_cells and n not in self.blocked_cells:
                    unvisited_neighbors.append(n)
            if len(unvisited_neighbors) == 0:
                stack.pop()
            else:
                next_cell = rand.choice(unvisited_neighbors)
                self.open_passage(current_cell, next_cell)
                visited_cells.add(next_cell)
                stack.append(next_cell)

        if not self.config.perfect:
            self.remove_dead_ends()

    def get_open_neighbors(self,
                           coordinates: tuple[int, int]
                           ) -> list[tuple[int, int]]:
        """
            Purpose: Find neighboring cells reachable through open passages.
            Args: coordinates — coordinates of the cell.
            Returns: A list of reachable neighboring coordinates.
        """

        open_neighbors: list[tuple[int, int]] = []
        x, y = coordinates

        if y > 0 and self.grid[y][x] & NORTH == 0:
            open_neighbors.append((x, y - 1))

        if x < self.config.width - 1 and self.grid[y][x] & EAST == 0:
            open_neighbors.append((x + 1, y))

        if y < self.config.height - 1 and self.grid[y][x] & SOUTH == 0:
            open_neighbors.append((x, y + 1))

        if x > 0 and self.grid[y][x] & WEST == 0:
            open_neighbors.append((x - 1, y))

        return open_neighbors

    def find_shortest_path(self) -> list[tuple[int, int]]:
        """
            Purpose: Find a shortest path from entry to exit using
            breadth-first search (BFS).
            Args: None.
            Returns: An ordered list of coordinates, including entry and exit.
            Returns an empty list if no path exists.
        """

        queue = deque([self.config.entry])
        visited_cells: set[tuple[int, int]] = set()
        visited_cells.add(self.config.entry)
        came_from: dict[tuple[int, int], tuple[int, int]] = {}

        while len(queue) != 0:
            current_cell = queue.popleft()
            if current_cell == self.config.exit:
                break
            open_neighbors = self.get_open_neighbors(current_cell)
            for n in open_neighbors:
                if n not in visited_cells:
                    visited_cells.add(n)
                    queue.append(n)
                    came_from[n] = current_cell
        if self.config.exit not in visited_cells:
            return []
        path: list[tuple[int, int]] = []
        curr_cell = self.config.exit
        while curr_cell != self.config.entry:
            path.append(curr_cell)
            curr_cell = came_from[curr_cell]
        path.append(curr_cell)
        path.reverse()
        return path

    def get_dead_ends(self) -> list[tuple[int, int]]:
        """
            Purpose: Find cells with exactly one open passage.
            Args: None.
            Returns: A list of dead-end coordinates.
        """
        dead_ends: list[tuple[int, int]] = []
        for y in range(self.config.height):
            for x in range(self.config.width):
                open_neighbors = self.get_open_neighbors((x, y))
                if len(open_neighbors) == 1:
                    dead_ends.append((x, y))

        return dead_ends

    def remove_dead_ends(self) -> None:
        """
            Purpose: Reduce dead ends by opening extra passages to eligible
            neighbors.
            Args: None.
            Returns: None; updates the grid.
            Note: Some dead ends may remain if no eligible neighbor exists.
        """
        dead_ends: list[tuple[int, int]] = self.get_dead_ends()
        rand = random.Random(self.config.seed)
        for end in dead_ends:
            neighbors = self.get_neighbors(end)
            open_neighbors = self.get_open_neighbors(end)
            if len(open_neighbors) != 1:
                continue
            candidates: list[tuple[int, int]] = []
            for n in neighbors:
                if n not in self.blocked_cells and n not in open_neighbors:
                    candidates.append(n)
            if len(candidates) != 0:
                candidate_cell = rand.choice(candidates)
                self.open_passage(end, candidate_cell)
            else:
                continue

    def get_path_directions(self) -> str:
        """
            Purpose: Convert the shortest path into movement directions.
            Args: None.
            Returns:A string containing N, E, S, and W. Returns an empty
            string if no path exists.
        """
        path = self.find_shortest_path()
        directions: list[str] = []
        for i in range(len(path) - 1):
            curr_x, curr_y = path[i]
            next_x, next_y = path[i + 1]

            x_diff = next_x - curr_x
            y_diff = next_y - curr_y

            if x_diff == 1 and y_diff == 0:
                directions.append('E')
            elif x_diff == -1 and y_diff == 0:
                directions.append('W')
            elif x_diff == 0 and y_diff == 1:
                directions.append('S')
            elif x_diff == 0 and y_diff == -1:
                directions.append('N')
        return "".join(directions)
