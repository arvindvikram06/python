from config import SERVICES


def get_target_service(path : str):
    parts = path.strip().split('/')

    if len(parts) < 2:
        return None
    
    service_key = parts[1]
    

    if service_key in SERVICES:
        base_url =  SERVICES[service_key]
        new_path = "/" + "/".join(parts[2:])
        return base_url + new_path
    
    return None