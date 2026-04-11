from config import SERVICES


def get_target_service(path: str):
    parts = path.strip("/").split("/")

    if len(parts) < 2:
        return None

    service_key = parts[1]

    if service_key in SERVICES:
        base_url = SERVICES[service_key]

        remaining_path = parts[2:]
        new_path = "/" + "/".join(remaining_path) if remaining_path else ""

        return base_url + new_path

    return None