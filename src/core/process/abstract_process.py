"""
This file holds the model architecture
"""

from abc import ABC, abstractmethod

class abstract_process(ABC):

    @abstractmethod
    def get_operator(self):
        pass

    @abstractmethod
    def log_model(self):
        pass

    @abstractmethod
    def serve_model(self):
        pass

    @abstractmethod
    def get_dag(self):
        pass
