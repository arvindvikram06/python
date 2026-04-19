from core.plugin_base import PluginBase

class BrokenPlugin(PluginBase):
    name = "broken-plugin"
    version = "1.0.0"
    dependencies = []

    def activate(self):
        print("[PLUGIN] Broken plugin starting...")
        raise Exception("Something went wrong!")

    def deactivate(self):
        print("[PLUGIN] Broken plugin stopped")