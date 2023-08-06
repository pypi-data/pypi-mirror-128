from .element import Element
from .group import Group
from .node import Node
from .topic import Topic
from .exercise import Exercise
from .task import Task
from . import errors
from . import element

from networkx.algorithms.dag import descendants
from networkx import DiGraph
from networkx.exception import NetworkXError


class Soup:
    def __init__(self, elements = None):
        self._elements = set()
        self._root_group = None
        self._worldgraph = None

        if elements: 
            for e in elements:
                self.add_element(e)
            self.commit()

    def __len__(self):
        # well this is a bit dumb
        return len(list(self._root_group.iter_recursive(userdata=self._userdata)))

    def add_element(self, element):
        assert isinstance(element, Element), element
        self._assert_uncommitted()
        if self._worldgraph:
            raise errors.OpenTrainingError(f'cannot add {element}: graph already made')
        self._elements.add(element)

    def committed(self):
        return self._root_group is not None

    def commit(self):
        if self._root_group is not None:
            return

        elements_to_resolve = list(self._elements)

        # build up hierarchy (thereby emptying self._elements)
        self._root_group = Group(
            title='Root', 
            path=(), 
            docname='', 
            userdata=None,
        )
        self._make_hierarchy()
        self._add_nodes_to_groups()
        assert len(self._elements) == 0, self._elements

        # once the elements have paths in their final hierarchy, we
        # can let them resolve their own stuff. for example, a task
        # initially refers to a person's *path* - final situation
        # should be though that a task refers to the person directly.
        errs = []
        for element in elements_to_resolve:
            try:
                element.resolve_paths(self)
            except errors.OpenTrainingError as e:
                errs.append(e)

        if len(errs):
            raise errors.CompoundError(
                'there were errors resolving paths of some elements', errors=errs, 
                # don't know which thing I could refer to when doing a
                # global resolve.
                userdata=None,
            )

        del self._elements
        self.worldgraph()    # only to detect missing dependencies
                             # early

    @property
    def root(self):
        return self._root_group

    def element_by_path(self, path, userdata):
        return self._root_group.element_by_path(path, userdata=userdata)

    def worldgraph(self):
        self._assert_committed()
        return self._make_worldgraph()

    def subgraph(self, entrypoints, userdata):
        '''Given entrypoints, compute a subgraph of the world graph that
        contains the entrypoints and all their descendants.

        entrypoints is an iterable of element paths or elements (can
        be mixed)
        '''

        # paranoia
        for e in entrypoints:
            assert isinstance(e, Element)

        self._assert_committed()
        world = self._make_worldgraph()

        topics = set()
        for topic in entrypoints:
            topics.add(topic)
            topics.update(descendants(world, topic))
        return world.subgraph(topics)

    def _make_worldgraph(self):
        if self._worldgraph is not None:
            return self._worldgraph

        collected_errors = []
        self._worldgraph = DiGraph()
        for elem in self._root_group.iter_recursive(cls=Node, userdata=None):
            if not isinstance(elem, Node):
                continue
            self._worldgraph.add_node(elem)
            for target_path in elem.dependencies:
                try:
                    target_topic = self.element_by_path(target_path, userdata=elem.userdata)
                    self._worldgraph.add_edge(elem, target_topic)
                except errors.PathNotFound as e:
                    collected_errors.append(
                        errors.DependencyError(
                            f'{elem.docname} ({elem}): dependency {target_path} not found', 
                            userdata=elem))

        if len(collected_errors) != 0:
            raise errors.CompoundError('cannot build world graph', errors=collected_errors, 
                                       # don't know which thing I could refer to when doing a
                                       # global resolve.
                                       userdata=None,
                                      )
        return self._worldgraph

    def _make_hierarchy(self):
        level = 1
        while True:
            all_groups = [g for g in self._elements if isinstance(g, Group)]
            if not all_groups:   # no more groups
                break
            level_groups = [g for g in all_groups if len(g._requested_path) == level]
            for g in level_groups:
                self._root_group.add_element(g, userdata=None)
                self._elements.remove(g)
            level += 1

    def _add_nodes_to_groups(self):
        nodes = [n for n in self._elements if isinstance(n, Node)]
        for n in nodes:
            self._root_group.add_element(n, userdata=None)
            self._elements.remove(n)
            
    def _assert_committed(self):
        if not self.committed():
            raise errors.NotCommitted('soup not committed')

    def _assert_uncommitted(self):
        if self.committed():
            raise errors.AlreadyCommitted('soup already committed')
