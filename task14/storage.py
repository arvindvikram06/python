import json

def save_graph(graph):
    with open("output/crawl_graph.json", "w") as f:
        json.dump(graph, f, indent=2)

def save_sitemap(urls):
    with open("output/sitemap.xml", "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

        for url in urls:
            f.write(f"<url><loc>{url}</loc></url>\n")

        f.write("</urlset>")