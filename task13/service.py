from collections import defaultdict

def process_data(data):
    total_revenue = sum(d["revenue"] for d in data)# Calculate total revenue by summing the "revenue" field from each data entry
    total_units = sum(d["units"] for d in data) # Calculate total units by summing the "units" field from each data entry

    avg_order_value = total_revenue / total_units if total_units else 0 

    region_data = defaultdict(int)
    for d in data:
        region_data[d["region"]] += d["revenue"] # Aggregate revenue by region

    west_decline = None
    if region_data.get("West", 0) < 200000: 
        west_decline = 12 # If the revenue for the "West" region is less than 200,000, set west_decline to 12

    return {
        "total_revenue": total_revenue,
        "total_units": total_units,
        "avg_order_value": round(avg_order_value, 2),
        "region_data": dict(region_data),
        "west_decline": west_decline
    } 