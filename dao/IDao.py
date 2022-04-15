from abc import ABCMeta, abstractmethod


class IDao(metaclass=ABCMeta):
    @abstractmethod
    def queryItem(self, item):
        pass

    @abstractmethod
    def addItem(self, item):
        pass

    @abstractmethod
    def modItem(self, item):
        pass
