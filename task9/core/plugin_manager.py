from core.plugin_base import PluginBase
import os
import importlib.util

class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.load_order = []
        self.failed_plugins = set()

    def load_plugins(self, plugin_dir="plugins"):
        print(f"[CORE] Scanning plugin directory: ./{plugin_dir}/")

        for file in os.listdir(plugin_dir):
            if file.endswith(".py"):
                file_path = os.path.join(plugin_dir, file)

                spec = importlib.util.spec_from_file_location(file[:-3], file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                for attr in dir(module):
                    obj = getattr(module, attr)

                    if isinstance(obj, type) and issubclass(obj, PluginBase) and obj != PluginBase:
                        plugin = obj()
                        self.plugins[plugin.name] = plugin
                        print(f"[CORE] Discovered plugin: {plugin.name}")

    def resolve_dependencies(self):
        print("[CORE] Resolving dependencies...")

        visited = {}
        stack = []

        def visit(plugin_name):
            if plugin_name in visited:
                if visited[plugin_name] == "visiting":
                    raise Exception(f"Circular dependency detected: {plugin_name}")
                return

            visited[plugin_name] = "visiting"

            plugin = self.plugins.get(plugin_name)
            if not plugin:
                raise Exception(f"Missing dependency: {plugin_name}")

            for dep in plugin.dependencies:
                visit(dep)

            visited[plugin_name] = "visited"
            stack.append(plugin_name)

        for plugin_name in self.plugins:
            visit(plugin_name)

        self.load_order = stack

    def activate_all(self):
        print("[CORE] Activating plugins in order...")

        for name in self.load_order:
            plugin = self.plugins[name]

            try:
                print(f"[CORE] Activating {name}...")
                result = plugin.activate()
                plugin.active = True

                if result:
                    print(f"[CORE] -> registered: {result}")

            except Exception as e:
                print(f"[ERROR] Failed to activate {name}: {e}")
                self.failed_plugins.add(name)

    def deactivate_all(self):
        print("[CORE] Deactivating plugins...")

        for name in reversed(self.load_order):
            plugin = self.plugins[name]

            if plugin.active:
                try:
                    print(f"[CORE] Deactivating {name}...")
                    plugin.deactivate()
                except Exception as e:
                    print(f"[ERROR] Failed to deactivate {name}: {e}")