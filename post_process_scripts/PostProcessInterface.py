from abc import ABC, abstractmethod

class PostProcessInterface(ABC):
    @abstractmethod
    def run(self):
        pass