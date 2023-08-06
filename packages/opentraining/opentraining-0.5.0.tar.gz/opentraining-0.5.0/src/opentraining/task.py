from .node import Node
from .element import verify_is_path
from . import errors


class Task(Node):
    IMPLEMENTATION, DOCUMENTATION, INTEGRATION = range(3)

    def __init__(self, 
                 title, path, docname, 
                 dependencies, userdata,

                 implementation_points, implementors,
                 documentation_points, documenters,
                 integration_points, integrators):

        if len(implementors) != 0:
            assert sum(share for person, share in implementors) <= 100
        if len(documenters) != 0:
            assert sum(share for person, share in documenters) <= 100
        if len(integrators) != 0:
            assert sum(share for person, share in integrators) <= 100

        # in tests this is easily gotten wrong
        for p,_ in implementors: verify_is_path(p, userdata=userdata)
        for p,_ in documenters: verify_is_path(p, userdata=userdata)
        for p,_ in integrators: verify_is_path(p, userdata=userdata)

        super().__init__(
            title=title, 
            path=path, 
            docname=docname, 
            # add persons as task dependencies
            dependencies=dependencies + [person for person, share in implementors + documenters + integrators], 
            userdata=userdata)

        self.implementation_points = implementation_points
        self.documentation_points = documentation_points
        self.integration_points = integration_points

        self.implementors = implementors
        self.documenters = documenters
        self.integrators = integrators

        self.resolved = False

    def resolve_paths(self, soup):
        errs = []
        resolved_implementors = []
        resolved_documenters = []
        resolved_integrators = []

        for person_path, share in self.implementors:
            try:
                person = soup.element_by_path(person_path, userdata=self.userdata)
                resolved_implementors.append((person, share))
            except errors.OpenTrainingError as e:
                errs.append(e)
        for person_path, share in self.documenters:
            try:
                person = soup.element_by_path(person_path, userdata=self.userdata)
                resolved_documenters.append((person, share))
            except errors.OpenTrainingError as e:
                errs.append(e)
        for person_path, share in self.integrators:
            try:
                person = soup.element_by_path(person_path, userdata=self.userdata)
                resolved_integrators.append((person, share))
            except errors.OpenTrainingError as e:
                errs.append(e)

        if errs:
            raise errors.CompoundError(f'could not resolve some paths of {self}', errs, userdata=None)

        self.implementors = resolved_implementors
        self.documenters = resolved_documenters
        self.integrators = resolved_integrators

        self.resolved = True

    def person_implementation_score(self, person):
        return self._person_score(person, self.IMPLEMENTATION)
    def person_documentation_score(self, person):
        return self._person_score(person, self.DOCUMENTATION)
    def person_integration_score(self, person):
        return self._person_score(person, self.INTEGRATION)

    def _person_score(self, person, what):
        assert self.resolved

        if what == self.IMPLEMENTATION:
            workers = self.implementors
            difficulty = self.implementation_points
        elif what == self.DOCUMENTATION:
            workers = self.documenters
            difficulty = self.documentation_points
        elif what == self.INTEGRATION:
            workers = self.integrators
            difficulty = self.integration_points
        else: assert False, what

        score = 0
        for p, share in workers:
            if person is p:
                score += share * difficulty
        return score
        
