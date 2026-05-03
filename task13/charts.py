import matplotlib.pyplot as plt
import os

def generate_bar_chart(region_data):
    os.makedirs("charts", exist_ok=True)

    regions = list(region_data.keys())
    values = list(region_data.values())

    path = "charts/bar.png"

    plt.figure()
    plt.bar(regions, values)
    plt.title("Revenue by Region")
    plt.savefig(path)
    plt.close()
    return path