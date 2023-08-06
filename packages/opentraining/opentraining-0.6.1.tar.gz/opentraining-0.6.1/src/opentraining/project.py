from .element import Element
from .person import Person
from .task import Task
from .group import Group

from collections import defaultdict
import itertools


class Project(Element):

    def __init__(self, title, path, docname, userdata,                 
                 persons, tasks):
        super().__init__(title=title, path=path, docname=docname, userdata=userdata)
        self.persons = persons
        self.tasks = tasks

    def score_table(self):
        'Return iterable of (person, points)'
        assert self.resolved

        points_per_person = defaultdict(int)

        for task in self.tasks:
            for person, share in task.implementors:
                points = share * task.implementation_points
                points_per_person[person] += points
            for person, share in task.documenters:
                points = share * task.documentation_points
                points_per_person[person] += points
            for person, share in task.integrators:
                points = share * task.integration_points
                points_per_person[person] += points

        return ((person, points_per_person[person]) for person in self.persons)

    def person_score(self, person):
        assert self.resolved
        assert type(person) is Person
        assert person in self.persons, (person.path, self.persons)

        score = 0

        for task in self.tasks:
            for p, share in task.implementors:
                if p is person:
                    score += task.implementation_points * share
            for p, share in task.documenters:
                if p is person:
                    score += task.documentation_points * share
            for p, share in task.integrators:
                if p is person:
                    score += task.integration_points * share

        return score

    def tasks_of_person(self, person):
        assert self.resolved
        assert type(person) is Person
        assert person in self.persons

        her_tasks = set()
        for task in self.tasks:
            if person in (p for p,_ in itertools.chain(task.implementors, task.documenters, task.integrators)):
                her_tasks.add(task)
        return her_tasks

    def resolve(self, soup):
        persons = []
        tasks = []
        for person in self.persons:
            if type(person) is Person:
                persons.append(person)
            else:
                elem = soup.element_by_path(person, userdata=self.userdata)
                if isinstance(elem, Person):
                    persons.append(elem)
                elif isinstance(elem, Group):
                    persons.extend(elem.iter_recursive(cls=Person))

        for task in self.tasks:
            if type(task) is Task:
                tasks.append(task)
            else:
                elem = soup.element_by_path(task, userdata=self.userdata)
                if isinstance(elem, Task):
                    tasks.append(elem)
                elif isinstance(elem, Group):
                    tasks.extend(elem.iter_recursive(cls=Task))
        
        self.persons = persons
        self.tasks = tasks

        super().resolve(soup)
