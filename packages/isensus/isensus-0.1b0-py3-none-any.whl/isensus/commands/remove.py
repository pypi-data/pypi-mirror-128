from ..data import Data


def remove(usertip: str) -> User:
    """ Removes a user from the database.

    Reads data from the json file, find the corresponding
    user and removes it from the data.

    Parameters
    ----------
    usertip: str
        First letters of the user's userid, lastname or firstname

    Returns
    -------
    user: User
        Instance of the removed user
    """

    with Data() as users:
        user = User.find_user(users, usertip)
        del users[user.userid]

    return user
