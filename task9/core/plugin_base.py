from abc import ABC, abstractmethod

class PluginBase(ABC):
    name = "base-plugin"
    version = "1.0.0"
    dependencies = []

    @abstractmethod
    def activate(self):
        raise NotImplementedError

    @abstractmethod
    def deactivate(self):
        pass    