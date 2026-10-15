def get_pattern_cells(width: int, height: int) -> set[tuple[int, int]]:
    """
        Purpose: Calculate the coordinates forming the centered “42” pattern.
        Args:
        - width: Number of maze columns.
        - height: Number of maze rows.
        Returns: A set of pattern coordinates, or an empty set if the maze is
        too small.
    """
    pattern_cells: set[tuple[int, int]] = set()
    if width < 13 or height < 7:
        return pattern_cells

    x = width // 2  # center_x
    y = height // 2  # center_y

    # number 2
    pattern_cells.add((x+1, y))
    pattern_cells.add((x+2, y))
    pattern_cells.add((x+3, y))
    pattern_cells.add((x+4, y))
    pattern_cells.add((x+4, y-1))
    pattern_cells.add((x+4, y-2))
    pattern_cells.add((x+3, y-2))
    pattern_cells.add((x+2, y-2))
    pattern_cells.add((x+1, y-2))
    pattern_cells.add((x+1, y+1))
    pattern_cells.add((x+1, y+2))
    pattern_cells.add((x+2, y+2))
    pattern_cells.add((x+3, y+2))
    pattern_cells.add((x+4, y+2))

    # number 4
    pattern_cells.add((x-1, y))
    pattern_cells.add((x-1, y-1))
    pattern_cells.add((x-1, y-2))
    pattern_cells.add((x-1, y+1))
    pattern_cells.add((x-1, y+2))
    pattern_cells.add((x-2, y))
    pattern_cells.add((x-3, y))
    pattern_cells.add((x-4, y))
    pattern_cells.add((x-4, y-1))
    pattern_cells.add((x-4, y-2))

    return pattern_cells
