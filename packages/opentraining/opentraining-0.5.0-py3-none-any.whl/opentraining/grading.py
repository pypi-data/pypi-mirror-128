from collections import defaultdict
import itertools


class Grading:

    def __init__(self, persons, tasks, userdata):
        self.persons = persons
        self.tasks = tasks
        self.userdata = userdata

    def score_table(self):
        'Return iterable of (person, points)'

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
        assert person in self.persons

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
        assert person in self.persons

        her_tasks = set()
        for task in self.tasks:
            if person in (p for p,_ in itertools.chain(task.implementors, task.documenters, task.integrators)):
                her_tasks.add(task)
        return her_tasks
