from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

class RobotsHandler:
    def __init__(self, base_url):
        parsed = urlparse(base_url)
        self.robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        self.parser = RobotFileParser()

    async def load(self):
        self.parser.set_url(self.robots_url)
        self.parser.read()

    def allowed(self, url):
        return self.parser.can_fetch("*", url)