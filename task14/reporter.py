def generate_report(results, inbound_count, seed):
    broken = []
    redirects = {}
    orphan = []

    for url, data in results.items():
        if data["status"] == 404:
            broken.append(url)

        if len(data["redirects"]) > 0:
            redirects[url] = data["redirects"]

    for url in results:
        if inbound_count[url] == 0 and url != seed:
            orphan.append(url)

    return broken, redirects, orphan