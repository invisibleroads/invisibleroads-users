from abc import ABCMeta, abstractmethod
from six import add_metaclass


@add_metaclass(ABCMeta)
class InvisibleRoadsScript(object):

    priority = 100

    @abstractmethod
    def configure(self, argument_subparser):
        pass

    @abstractmethod
    def run(self, arguments):
        pass
