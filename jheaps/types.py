from abc import ABC, abstractmethod
from collections.abc import Mapping

from .backend import HeapType


class GraphPath(ABC):
    """Interface for a graph path."""

    @abstractmethod
    def weight(self):
        """Weight of the path.

        :rtype: Double
        """
        pass

    @abstractmethod
    def start_vertex(self):
        """Starting vertex of the path."""
        pass

    @abstractmethod
    def end_vertex(self):
        """Ending vertex of the path."""
        pass

    @abstractmethod
    def edges(self):
        """Edges of the path.

        :rtype: :class:`collections.abc.Iterable`
        """
        pass

    @abstractmethod
    def graph(self):
        """The graph that this graph path refers to.

        :rtype: :class:`jgrapht.types.Graph`
        """
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @property
    def vertices(self):
        """Vertices of the path."""
        v_list = []

        if len(self.edges) == 0:
            start = self.start_vertex
            if start is not None and start == self.end_vertex:
                v_list.append(start)
            return v_list

        v = self.start_vertex
        v_list.append(v)
        for e in self.edges:
            v = self.graph.opposite(e, v)
            v_list.append(v)

        return v_list


