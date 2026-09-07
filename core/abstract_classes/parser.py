from abc import ABC, abstractmethod

class Parser(ABC):
    @abstractmethod
    def to_symbolic_expression(self, f : str):
        pass

    @abstractmethod
    def to_python_function(self, f, variable_list):
        pass

