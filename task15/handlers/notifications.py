from events.events import OrderPlaced

# Sends external notifications
class NotificationService:
    async def handle(self, event):
        if isinstance(event, OrderPlaced):
            print("[HANDLER: Notification] Sending email...")
            print(f"Email sent to {event.customer}")