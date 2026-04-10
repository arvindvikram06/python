import time, random

def send_email(to, template):
    if random.random() < 0.7:
        raise Exception("SMTPConnectionError")
    return "email_sent"

def generate_thumbnail(image_id, size):
    time.sleep(1)
    return f"/thumbs/{image_id}_{size[0]}x{size[1]}.jpg"