from dataclasses import dataclass
from shutil import get_terminal_size


@dataclass
class MazeConfig:
    """
        Purpose: Store the settings used to generate and save a maze.
        Attributes:
        - width: Number of maze columns.
        - height: Number of maze rows.
        - entry: Starting cell coordinates (x, y).
        - exit: Destination cell coordinates (x, y).
        - output_file: Path where the maze is saved.
        - perfect: Whether to generate a maze without loops.
        - seed: Optional integer for reproducible generation; defaults to None.
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None


def read_config_file(filepath: str) -> dict[str, str]:

    """
        Purpose: Read the configuration file and check its basic format.
        Args: filepath — path to the configuration file.
        Returns: A dictionary containing string keys and string values.
        Raises:
        - ValueError — invalid lines, empty keys or values, duplicate keys, or
         missing required keys.
        - OSError — the file cannot be opened or read.
    """

    required_keys: list[str] = ["WIDTH", "HEIGHT",
                                "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    with open(filepath, 'r') as file:
        my_dict: dict[str, str] = {}
        for line in file:
            new_line: str = line.strip()
            if (new_line.startswith('#') or not new_line):
                continue
            if '=' in new_line:
                wlist: list[str] = new_line.split('=', 1)
                key = wlist[0].strip().upper()
                value = wlist[1].strip()
                if not key or not value:
                    raise ValueError("Missing Values/Keys")
                if key in my_dict:
                    raise ValueError(f"{key} key is duplicated")
                else:
                    my_dict[key] = value

            else:
                raise ValueError(f"Invalid Format {new_line}")
        for key in required_keys:
            if key not in my_dict:
                raise ValueError(f"{key} key is missed")
        for key in key.lower():
            if key == key.lower():
                key = key.upper()
    return my_dict


def parse_positive_int(key: str, value: str) -> int:
    """
        Purpose: Convert a string to an integer and check that it is positive.
        Args:
        - key: Configuration key used in error messages.
        - value: String to convert.

        Returns: An integer greater than zero.
        Raises: ValueError if the string cannot be converted or the integer is
        zero or negative.
    """
    try:
        val = int(value)
    except ValueError:
        raise ValueError(f"Value {value} for '{key}' is INVALID")
    if val <= 0:
        raise ValueError(f"{key} must be a positive value")
    return val


def parse_coordinates(width: int,
                      height: int, key: str, value: str) -> tuple[int, int]:
    """
        Purpose: Convert an x,y string into coordinates and check maze bounds.
        Args:
        - width: Number of maze columns.
        - height: Number of maze rows.
        - key: Configuration key, such as ENTRY or EXIT,
        used in error messages.
        - value: Coordinate string to parse.
        Returns: A tuple containing the integer coordinates (x, y).
        Raises: ValueError if the format is invalid or coordinates are outside
        the maze
    """

    coordinates: list[str] = value.split(',')
    if len(coordinates) != 2:
        raise ValueError(f"{key} value is invalid")
    try:
        x = int(coordinates[0])
        y = int(coordinates[1])
    except ValueError:
        raise ValueError(f"Invalid coordinates {value} for {key}")
    if x < 0 or x > width - 1 or y < 0 or y > height - 1:
        raise ValueError(f"Out of range coordinates for {key}")
    return (x, y)


def parse_config(mydict: dict[str, str]) -> MazeConfig:
    """
        Purpose: Convert configuration strings into validated maze settings.
        Args: mydict — dictionary containing configuration keys and string
        values.
        Returns: A MazeConfig object containing the parsed settings.
        Raises:
        - ValueError — invalid dimensions, coordinates, mode, or seed;
        matching entry and exit; or an unsupported size for non-perfect mode.
        - KeyError — a required key is missing when the function is called
        directly.
    """

    width = parse_positive_int("WIDTH", mydict['WIDTH'])
    height = parse_positive_int("HEIGHT", mydict['HEIGHT'])
    terminal_size = get_terminal_size()
    if width > terminal_size.columns and height > terminal_size.lines:
        raise ValueError("Maze size cannot exceed terminal size")

    entry_val = parse_coordinates(width,
                                  height, "ENTRY", mydict['ENTRY'])
    exit_val = parse_coordinates(width, height, "EXIT", mydict['EXIT'])

    if (entry_val == exit_val):
        raise ValueError("ENTRY and EXIT cannot be the same value")
    perfect_text = mydict["PERFECT"].lower()
    if perfect_text == "true":
        perfect_val = True
    elif perfect_text == "false":
        perfect_val = False
        if width == 1 or height == 1 or width == 2 and height == 2:
            raise ValueError("Invalid maze size for PERFECT=FALSE mode")
    else:
        raise ValueError("Invalid value for 'PERFECT' key")
    seed_val = None
    if "SEED" in mydict:
        try:
            seed_val = int(mydict['SEED'])
        except ValueError:
            raise ValueError("Invalid SEED value")

    maze_obj = MazeConfig(height=height, width=width, entry=entry_val,
                          exit=exit_val, output_file=mydict['OUTPUT_FILE'],
                          perfect=perfect_val, seed=seed_val)

    return maze_obj
