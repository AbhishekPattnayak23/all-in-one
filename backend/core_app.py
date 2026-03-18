# backend/core_app.py - Core application logic
from typing import Optional, Dict, Any
from backend.notifications.service import NotificationService

class Message:
    def __init__(self, receiver_id: int, sender, content: str):
        self.receiver_id = receiver_id
        self.sender = sender
        self.sender.username = getattr(sender, 'username', 'User')
        self.content = content
    def save(self):
        pass  # Database save operation

def complete_crud_operations(self, message: Message) -> Dict[str, Any]:
    """Complete CRUD operations for message handling"""
    message.save()

    notification = NotificationService()

    notification.send_email_notification(

        recipient_id=message.receiver_id,

        subject=f"New message from {getattr(message.sender, \"username\", message.sender.__dict__.get(\"username\", \"User\"))}",

        body=message.content

    )

    notification.push_notification(

        recipient_id=message.receiver_id,

        title="New chat message",

        message=message.content

    )
    return {"status": "success", "message": message}

def handle_websocket_message(message_data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle websocket incoming messages"""
    message = Message(
        receiver_id=message_data['receiver_id'],
        sender=message_data['sender'],
        content=message_data['content']
    )
    message.save()

    notification = NotificationService()

    notification.send_email_notification(

        recipient_id=message.receiver_id,

        subject=f"New message from {getattr(message.sender, \"username\", message.sender.__dict__.get(\"username\", \"User\"))}",

        body=message.content

    )

    notification.push_notification(

        recipient_id=message.receiver_id,

        title="New chat message",

        message=message.content

    )
    return {"status": "delivered", "message": message}

def process_new_message(message_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process new message from channel consumers"""
    message = Message(
        receiver_id=message_data['receiver_id'],
        sender=message_data['sender'],
        content=message_data['content']
    )
    message.save()

    notification = NotificationService()

    notification.send_email_notification(

        recipient_id=message.receiver_id,

        subject=f"New message from {getattr(message.sender, \"username\", message.sender.__dict__.get(\"username\", \"User\"))}",

        body=message.content

    )

    notification.push_notification(

        recipient_id=message.receiver_id,

        title="New chat message",

        message=message.content

    )
    return {"status": "processed", "message": message}
