import logging


from robot.api.deco import library  # , keyword

# https://developer.microsoft.com/en-us/graph/quick-start


@library(scope="GLOBAL", doc_format="REST", auto_keywords=False)
class Graph:
    """Library for Microsoft Graph API


    **Examples**

    .. code:: robotframework

        *** Settings ***
        Library   RPA.Microsft.Graph

        *** Tasks ***
        Access email
            No Operation

        Access sharepoint
            No Operation

    .. code:: python

        from RPA.Microft.Graph import Graph

    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
