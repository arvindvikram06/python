from core.plugin_base import PluginBase

class LoggerPlugin(PluginBase):
    name = "Logger Plugin"

    def activate(self):
        print("[Logger] Plugin activated!")

    def deactivate(self):
        print("[Logger] Plugin deactivated!")