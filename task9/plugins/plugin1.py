from core.plugin_base import PluginBase

class MarkdownParser(PluginBase):
    name = "markdown-parser"
    version = "1.0.0"
    dependencies = []

    def activate(self):
        print("[PLUGIN] MarkdownParser activated")
        return "markdown → HTML converter"

    def deactivate(self):
        pass


class RssFeedPlugin(PluginBase):
    name = "rss-feed"
    version = "1.0.0"
    dependencies = ["markdown-parser"]

    def activate(self):
        print("[PLUGIN] RSS Feed Plugin activated")
        return "RSS generator"

    def deactivate(self):
        pass