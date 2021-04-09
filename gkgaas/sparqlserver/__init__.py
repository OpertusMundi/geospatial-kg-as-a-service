from abc import ABC, abstractmethod


class SPARQLServer(ABC):
    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def stop(self):
        pass
