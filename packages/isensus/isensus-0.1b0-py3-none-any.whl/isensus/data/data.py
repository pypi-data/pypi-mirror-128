""" Path the default json database file
"""

import json, typing
from pathlib import Path
from .user import User

json_file_path_g = Path.home() / ".isensus"

def set_json_path(path: Path) -> None:
    """ Set the path to the json database
    
    The function get_data, that is used accross all commands,
    uses the json file path to read the database of users.
    If this function is never called, ~/.isensus is used.

    Parameters
    ----------
    path: Path
        path to the json database file to user of the whole package
    """
    global json_file_path_g
    json_file_path_g = path


def _get_data_path(path: Path) -> Path:
    """ Returns the path to the json database,
    initialize it if it does not exit yet.

    Parameters
    ----------
    path: Path 
        Path to the json database
    """
    if not path.is_file():
        with open(path, "w") as jsonfile:
            json.dump({}, jsonfile)
    return path


def _read_json_file(path: Path) -> typing.Dict[str,str]:
    # Attempt to parse the file provided by the path,
    # returning a (json serialized) dict or raising a
    # FileNotFoundError or a ValueError
    if not path.is_file():
        raise FileNotFoundError(
            "failed to find isensus " "data file: {}".format(json_path)
        )
    try:
        with open(path) as f:
            data = json.load(f)
    except Exception as e:
        raise ValueError(
            "failed to parse isensus json " "data file {}: {}".format(path, e)
        )
    return data

def get_data() -> typing.Dict[str, User]:
    """ Read the json file database

    Reads the json data file (~/.isensus by default) and
    return the corresponding instances of User.
    The method set_json_path should be called to change 
    the path to the json database used.

    Returns
    -------
    users: dict
        userids (str) as keys, instances of User as
        values.
    """
    path = _get_data_path(json_file_path_g)
    json_content = _read_json_file(path)
    return User.from_json(json_content)


def write_data(users: typing.Dict[str, User]) -> None:
    """
    Writes the users in the json data file
    (~/.isensus).
    """
    path = _get_data_path(json_file_path_g)
    json_content = User.to_json(users)
    with open(path, "w") as f:
        f.write(json_content)


class Data:
    """ Context manager for json database file.

    Context manager that will read the data json file
    (~/.isensus) when entering, returning the 
    corresponding dictionary {userid: instance of User}.
    At exit, this dictionary is written back in the data
    file. Hence, the returned dictionary is mutabled, and
    users are expected to modify it.
    """

    def __init__(self):
        pass

    def __enter__(self) -> typing.Dict[str, User]:
        self._users = get_data()
        return self._users

    def __exit__(self, type, value, traceback):
        write_data(self._users)
