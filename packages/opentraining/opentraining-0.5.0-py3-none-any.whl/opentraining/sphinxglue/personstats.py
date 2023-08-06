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
    app.add_directive('ot-personstats', _PersonStatsDirective)
    app.connect('doctree-resolved', _ev_doctree_resolved__expand_personstats_nodes)

def _ev_doctree_resolved__expand_personstats_nodes(app, doctree, docname):
    for n in doctree.traverse(_PersonStatsNode):
        person = app.ot_soup.element_by_path(n.person, userdata=n)
        tasks = []
        for task in n.tasks:
            try:
                elem = app.ot_soup.element_by_path(task, userdata=n)
                if isinstance(elem, Task):
                    tasks.append(elem)
                elif isinstance(elem, Group):
                    tasks.extend(elem.iter_recursive(cls=Task, userdata=n))
            except OpenTrainingError as e:
                _logger.warning(e, location=n)

        grading = Grading(persons = [person], tasks = tasks, userdata = n)

        table = nodes.table()
        tgroup = nodes.tgroup(cols=5)
        table += tgroup
        tgroup += nodes.colspec(colwidth=8)
        tgroup += nodes.colspec(colwidth=4)
        tgroup += nodes.colspec(colwidth=4)
        tgroup += nodes.colspec(colwidth=4)
        tgroup += nodes.colspec(colwidth=4)

        if 'thead':
            thead = nodes.thead()
            tgroup += thead
            row = nodes.row()
            thead += row

            entry = nodes.entry()
            row += entry
            entry += nodes.Text('Task')

            entry = nodes.entry()
            row += entry
            entry += nodes.Text('Implementation')

            entry = nodes.entry()
            row += entry
            entry += nodes.Text('Documentation')

            entry = nodes.entry()
            row += entry
            entry += nodes.Text('Integration')
            
            entry = nodes.entry()
            row += entry
            entry += nodes.Text('Task total')

        if 'tbody':
            tbody = nodes.tbody()
            tgroup += tbody

            for task in grading.tasks_of_person(person):
                row = nodes.row()
                tbody += row

                # link to task
                entry = nodes.entry()
                row += entry
                p = nodes.paragraph()
                entry += p
                p += utils.make_reference(text=task.title, from_docname=docname, to_docname=task.docname, app=app)

                # points scored from that task
                implementation_score = task.person_implementation_score(person)
                documentation_score = task.person_documentation_score(person)
                integration_score = task.person_integration_score(person)
                total_score = implementation_score + documentation_score + integration_score

                entry = nodes.entry()
                row += entry
                entry += nodes.Text(str(implementation_score))

                entry = nodes.entry()
                row += entry
                entry += nodes.Text(str(documentation_score))

                entry = nodes.entry()
                row += entry
                entry += nodes.Text(str(integration_score))

                entry = nodes.entry()
                row += entry
                entry += nodes.Text(str(total_score))

            row = nodes.row()
            tbody += row

            entry = nodes.entry()
            row += entry
            entry += nodes.Text('Total Score')

            entry = nodes.entry()
            row += entry

            entry = nodes.entry()
            row += entry

            entry = nodes.entry()
            row += entry

            entry = nodes.entry()
            row += entry
            entry += nodes.Text(str(grading.person_score(person)))

        n.replace_self([table])

class _PersonStatsNode(nodes.Element):
    def __init__(self, person, tasks):
        super().__init__(self)
        self.title = None
        self.person = person
        self.tasks = tasks

class _PersonStatsDirective(SphinxDirective):
    required_arguments = 1   # person
    option_spec = {
        'tasks': utils.list_of_elementpath,
    }

    def run(self):
        person = utils.element_path(self.arguments[0].strip())
        tasks = self.options.get('tasks', [])

        scores = _PersonStatsNode(
            person = person,
            tasks = tasks,
        )

        scores.document = self.state.document
        set_source_info(self, scores)

        return [scores]
