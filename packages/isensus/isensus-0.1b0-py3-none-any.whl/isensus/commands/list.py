from isensus.data.data import Data


def list() -> None:
    """ Print the list of users included in the database
    """

    with Data() as users:
        attrs = ("firstname", "lastname")
        userids = sorted(users.keys())
        for userid, user in users.item():
            values = [getattr(user, attr) for attr in attrs]
            print(userid, "\t", "\t".join(values))
