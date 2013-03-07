# coding: utf-8

import numpy
from particles import PARTICLES, LIMIT, VOID, SAND

class Environment(object):
    """A particle system environment. Keeps a list of "active" particles to
       save processing when updating.
    """

    def __init__(self, width, height, implementation=PARTICLES,
                 initial_particle=VOID, limit_particle=LIMIT,
                 wrap_h=False, wrap_v=False):
        self.width = width
        self.height = height
        self.implementation = implementation
        self.matrix = numpy.empty((width, height))
        self.matrix.fill(initial_particle)
        self.limit_particle = limit_particle
        self.wrap_h = wrap_h
        self.wrap_v = wrap_v

        self.actives = set()
        self.changes = set()
        self.to_sleep = set()
        self.to_awake = set()

    def __setitem__(self, position, new_value):
        x, y = self.wrap(position)
        if self.is_inside((x, y)):
            self.changes.add(((x, y), new_value))

    def __getitem__(self, position):
        x, y = self.wrap(position)
        return self.matrix[x,y] if self.is_inside((x,y)) else self.limit_particle

    def wrap(self, position):
        """Return the "wrapped" version of the position, depending on the
           wrap settings of this environment.
        """
        x, y = position
        return (x % self.width  if self.wrap_h else x,
                y % self.height if self.wrap_v else y)

    def is_inside(self, position):
        """Return whether or not the position is inside the limit space.
        """
        return 0 <= position[0] < self.width and 0 <= position[1] < self.height

    def report_change(self, position, particle):
        """Report a change of value in this position to the new particle.
           This method is supposed to be implemented by GUI subclasses.
        """
        pass

    def step(self):
        """Updates all active particles once.
        """
        # update every active particle
        for position in self.actives:
            self.implementation[self.matrix[position]](self, position)

        # change particles that were marked for change
        for position, new_value in self.changes:
            self.matrix[position] = new_value
            self.report_change(position, new_value)

        # remove particles from active set that were marked for sleep
        self.actives.difference_update(self.to_sleep)

        # add particles to active set that were marked for awake
        self.actives.update(self.to_awake)

        # reset change queues
        self.to_awake.clear()
        self.to_sleep.clear()
        self.changes.clear()

    def awake(self, position):
        """Awake particle in position - adds it to the "active" list.
        """
        x, y = self.wrap(position)
        if self.is_inside((x, y)):
            self.to_awake.add((x, y))

    def sleep(self, position):
        """Sleeps particle in position - removes it from the "active" list.
        """
        x, y = self.wrap(position)
        if self.is_inside((x, y)):
            self.to_sleep.add((x, y))

