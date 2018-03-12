# This file is part of PJJobs project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

from pjjobs import PJJob


class TestBucle(PJJob):
    def __init__(self):
        super(TestBucle, self).__init__()

    def _run(self, data):
        i = 0
        while i < data['bucle']:
            print("{0}".format(i))
            i += 1


class TestBucleQueue(PJJob):
    def __init__(self):
        super(TestBucleQueue, self).__init__()

    def _run(self, data):
        i = 0
        while i < data['bucle']:
            print("queue: {0}".format(i))
            i += 1


class TestBucleQueue2(PJJob):
    def __init__(self):
        super(TestBucleQueue2, self).__init__()

    def _run(self, data):
        i = 0
        while i < data['bucle']:
            print("queue 2: {0}".format(i))
            i += 1
