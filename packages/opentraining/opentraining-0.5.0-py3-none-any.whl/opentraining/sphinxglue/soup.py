from ..soup import Soup
from ..element import Element
from ..topic import Topic
from ..exercise import Exercise
from ..task import Task
from ..group import Group
from .. import errors

from sphinx.util import logging
_logger = logging.getLogger(__name__)


def _prepare_app(app):
    if hasattr(app, 'ot_soup'):
        raise OpenTrainingError('Soup already created, cannot add one more element')
    if not hasattr(app.env, 'ot_elements'):
        app.env.ot_elements = {}

def sphinx_add_element(app, element):
    _prepare_app(app)
    assert isinstance(element, Element)
    app.env.ot_elements[element.docname] = element

def sphinx_purge_doc(app, env, docname):
    if hasattr(env, 'ot_elements'):
        env.ot_elements.pop(docname, None)

def sphinx_create_soup(app):
    if hasattr(app, 'ot_soup'):
        return

    app.ot_soup = Soup()
    for element in app.env.ot_elements.values():
        app.ot_soup.add_element(element)

    try:
        app.ot_soup.commit()
    except errors.CompoundError as e:
        for err in e:
            _logger.warning(str(err), location=err.userdata)
