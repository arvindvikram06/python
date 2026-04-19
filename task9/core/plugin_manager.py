import os
import importlib.util
from core.plugin_base import PluginBase

class PluginManager:
    def __init__(self):
        self.plugins = []

    def load_plugins(self, plugin_dir="plugins"):
        print(f"[CORE] Scanning plugin directory: ./{plugin_dir}/")

        for file in os.listdir(plugin_dir):
            if file.endswith(".py"):
                file_path = os.path.join(plugin_dir, file)

                spec = importlib.util.spec_from_file_location(file[:-3], file_path)
                # print("this is spec : ",spec)

                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # find classes inside module
                for attr in dir(module):
                    obj = getattr(module, attr)
                    
                    if isinstance(obj, type) and issubclass(obj, PluginBase) and obj != PluginBase:
                        plugin_instance = obj()
                        # print("this is plugin object",obj)
                        self.register(plugin_instance)

    def register(self, plugin):
        print(f"[CORE] Registering plugin: {plugin.name}")
        self.plugins.append(plugin)

    def activate_all(self):
        print("[CORE] Activating plugins...")
        for plugin in self.plugins:
            plugin.activate()