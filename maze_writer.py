def write_maze(output_file: str,
               grid: list[list[int]], entry: tuple[int, int],
               exit: tuple[int, int], directions: str) -> None:
    """
        Purpose: Save hexadecimal maze rows, entry, exit, and solution
        directions to a file.
        Args:
        - output_file: Destination file path.
        - grid: Rows of maze wall values.
        - entry: Starting coordinates.
        - exit: Destination coordinates.
        - directions: Shortest-path direction string.
        Returns: None.
        Raises: OSError if the file cannot be opened or written.
        Note: Replaces the contents of an existing destination file.
    """
    with open(output_file, 'w') as file:
        for row in grid:
            hex_digits: list[str] = []
            for cell in row:
                digit = format(cell, 'X')
                hex_digits.append(digit)
            hex_row_as_str = "".join(hex_digits) + '\n'
            file.write(hex_row_as_str)
        file.write('\n')
        x1, y1 = entry
        x2, y2 = exit
        file.write(f"{x1},{y1}\n")
        file.write(f"{x2},{y2}\n")
        file.write(f"{directions}\n")
