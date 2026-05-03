class PageData:
    def __init__(self, url, status, time_taken, redirects, final_url):
        self.url = url
        self.status = status
        self.time_taken = time_taken
        self.redirects = redirects
        self.final_url = final_url