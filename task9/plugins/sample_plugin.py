from core.plugin_base import PluginBase

class SamplePlugin(PluginBase):
    name = "sample-plugin"
    version = "1.0.0"
    dependencies = []

    def activate(self):
        print("[PLUGIN] SamplePlugin activated")

    def deactivate(self):
        print("[PLUGIN] SamplePlugin deactivated")