"""
This file holds the model architecture
"""

from abc import ABC, abstractmethod

class abstract_dag(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def set_processes(self):
        pass

    @abstractmethod
    def set_process_flow(self):
        pass


