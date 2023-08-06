from . import utils
from . import soup
from ..grading import Grading
from ..person import Person
from ..task import Task
from ..group import Group
from ..errors import OpenTrainingError

from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import set_source_info
from docutils import nodes
from docutils.parsers.rst import directives 


from sphinx.util import logging
_logger = logging.getLogger(__name__)


def setup(app):
    app.add_directive('ot-scoretable', _ScoreTableDirective)
    app.connect('doctree-resolved', _ev_doctree_resolved__expand_scoretable_nodes)

def _ev_doctree_resolved__expand_scoretable_nodes(app, doctree, docname):
    for n in doctree.traverse(_ScoreTableNode):
        persons = []
        tasks = []
        for person in n.persons:
            try:
                elem = app.ot_soup.element_by_path(person, userdata=n)
                if isinstance(elem, Person):
                    persons.append(elem)
                elif isinstance(elem, Group):
                    persons.extend(elem.iter_recursive(cls=Person, userdata=n))
            except OpenTrainingError as e:
                _logger.warning(e, location=n)
        for task in n.tasks:
            try:
                elem = app.ot_soup.element_by_path(task, userdata=n)
                if isinstance(elem, Task):
                    tasks.append(elem)
                elif isinstance(elem, Group):
                    tasks.extend(elem.iter_recursive(cls=Task, userdata=n))
            except OpenTrainingError as e:
                _logger.warning(e, location=n)

        grading = Grading(persons = persons, tasks = tasks, userdata = n)

        table = nodes.table()
        tgroup = nodes.tgroup(cols=2)
        table += tgroup
        tgroup += nodes.colspec(colwidth=8)
        tgroup += nodes.colspec(colwidth=4)

        thead = nodes.thead()
        tgroup += thead
        row = nodes.row()
        thead += row

        entry = nodes.entry()
        row += entry
        entry += nodes.Text('Person')
        entry = nodes.entry()
        row += entry
        entry += nodes.Text('Points')

        tbody = nodes.tbody()
        tgroup += tbody

        for person, points in sorted(grading.score_table(), key=lambda elem: (elem[0].lastname, elem[0].firstname)):
            row = nodes.row()
            tbody += row

            # link to person
            entry = nodes.entry()
            row += entry
            p = nodes.paragraph()
            entry += p
            if person.firstname and person.lastname:
                text = f' {person.lastname} {person.firstname}'
            else:
                text = person.title
            p += [utils.make_reference(text=text,
                                       from_docname=docname, to_docname=person.docname,
                                       app=app)]

            # points
            entry = nodes.entry()
            row += entry
            entry += nodes.Text(str(points))

        n.replace_self([table])

class _ScoreTableNode(nodes.Element):
    def __init__(self, persons, tasks):
        super().__init__(self)
        self.title = None
        self.persons = persons
        self.tasks = tasks

class _ScoreTableDirective(SphinxDirective):
    required_arguments = 0
    option_spec = {
        'persons': utils.list_of_elementpath,
        'tasks': utils.list_of_elementpath,
    }

    def run(self):
        persons = self.options.get('persons')
        tasks = self.options.get('tasks')

        scores = _ScoreTableNode(
            persons = persons,
            tasks = tasks,
        )

        scores.document = self.state.document
        set_source_info(self, scores)

        return [scores]
