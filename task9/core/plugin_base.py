from abc import ABC, abstractmethod

class PluginBase(ABC):
    name = "base-plugin"
    version = "1.0.0"
    dependencies = []

    def __init__(self):
        self.active = False

    @abstractmethod
    def activate(self):
        pass

    def deactivate(self):
        pass