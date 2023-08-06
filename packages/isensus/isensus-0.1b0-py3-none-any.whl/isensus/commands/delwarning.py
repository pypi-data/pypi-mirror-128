import typing
from isensus.data.data import Data
from isensus.data.user import User

def delwarning(usertip: str, index: int) -> User:
    """  Remove a user's warning
    
    Reads the data from the json file and find the user corresponding
    to the usertip. Then remove the entry corresponding to 
    the user's warning at the given index.
    Return the instance of User that has been updated.

    Parameters
    ----------
    usertip: str
        First letters of the user's userid, lastname or firstname
    index: int
        index of warnings or the notes to remove

    Returns
    -------
    user: User
        Instance of the updated user after update
    """
    with Data() as users:
        user = User.find_user(users)
        getattr(user, "warnings").rm(index)

    return user
