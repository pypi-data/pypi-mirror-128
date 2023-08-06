from . import utils
from . import soup
from ..project import Project
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
        try:
            project = app.ot_soup.element_by_path(n.path, userdata=n)
        except OpenTrainingError as e:
            _logger.warning(e, location=e.userdata)
            n.replace_self([])
            continue

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

        for person, points in sorted(project.score_table(), key=lambda elem: (elem[0].lastname, elem[0].firstname)):
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
    def __init__(self, path):
        super().__init__(self)
        self.path = path
        
class _ScoreTableDirective(SphinxDirective):
    required_arguments = 1   # path
    option_spec = {
        'sort-by': utils.list_of_elementpath,
    }

    def run(self):
        path = utils.element_path(self.arguments[0].strip())

        scores = _ScoreTableNode(path = path)
        scores.document = self.state.document
        set_source_info(self, scores)

        return [scores]
