from core.plugin_base import PluginBase

class AuthPlugin(PluginBase):
    name = "Auth Plugin"

    def activate(self):
        print("[Auth] Plugin activated!")

    def deactivate(self):
        print("[Auth] Plugin deactivated!")