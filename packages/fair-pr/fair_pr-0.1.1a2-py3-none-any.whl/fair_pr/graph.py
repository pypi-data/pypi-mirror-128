""" File contains all the graph structures.

TODO: Check what struct to use to escalate for big data.
Also check compatibility with networkx library
https://networkx.org/

Are sparse adjecency matrices equal to adjecency lists?
Can a simple dictionary be the best solution?
"""


class graph():
    """ The main graph class.

    The networks in the fair PageRank project are graphs with
    attributes on their nodes. In the simplest occasion this attribute
    is binary and represents a sensitive charakteristic of an individual.
    """
    def __init__(self, edge_file: str, attributes_file: str):
        """
        Args:
            edge_file:
            attributes_file:
        
        Example:
        """
        pass

