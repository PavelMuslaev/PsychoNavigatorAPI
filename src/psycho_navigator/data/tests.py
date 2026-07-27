from typing import TypedDict


class Test(TypedDict):
    """
    :param id: ID of the test.
    :param name: Name of the test.
    :param description: Description of the test.
    """

    id: int
    name: str
    description: str

