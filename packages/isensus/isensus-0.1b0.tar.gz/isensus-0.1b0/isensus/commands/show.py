from isensus.data.data import Data
from isensus.data.user import User


def show(usertip: str) -> User:

    """ Print all the value of all attributes of a specific user

    Reads data from the json file, find the user
    corresponding to the usertip, and print the 
    related attributes values.

    Parameters
    ----------
    usertip: str
        First letters of the user's userid, lastname or firstname

    Returns
    -------
    user: User
        Instance of the updated user after update

    """

    with Data() as users:
        user = User.find_user(users, usertip)

    print(user.to_string())
    return user
