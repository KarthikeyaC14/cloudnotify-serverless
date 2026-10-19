
import json
import re


ALLOWED_CHANNELS = {"email", "sms"}
MAX_MESSAGE_LENGTH = 1000


def response(status_code, body):
    """Create a response compatible with API Gateway."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body),
    }


def validate_notification(data):
    """Validate the notification request without sending it."""

    if not isinstance(data, dict):
        return None, "Request body must be a JSON object."

    name = data.get("recipientName")
    channel = data.get("channel")
    destination = data.get("destination")
    message = data.get("message")

    if not all(isinstance(value, str) for value in
               (name, channel, destination, message)):
        return None, "All fields must be provided as text."

    name = name.strip()
    channel = channel.strip().lower()
    destination = destination.strip()
    message = message.strip()

    if not name or len(name) > 100:
        return None, "Recipient name must contain 1–100 characters."

    if channel not in ALLOWED_CHANNELS:
        return None, "Channel must be email or sms."

    if not message or len(message) > MAX_MESSAGE_LENGTH:
        return None, "Message must contain 1–1000 characters."

    if channel == "email":
        valid_email = re.fullmatch(
            r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
            r"[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+",
            destination,
        )
        if not valid_email or len(destination) > 254:
            return None, "Enter a valid email address."

    if channel == "sms":
        if not re.fullmatch(r"\+[1-9]\d{7,14}", destination):
            return None, (
                "Enter a phone number with country code, "
                "for example +14155552671."
            )

    return {
        "recipientName": name,
        "channel": channel,
        "destination": destination,
        "message": message,
    }, None


def lambda_handler(event, context):
    """AWS Lambda entry point."""

    try:
        body = event.get("body", event)

        if isinstance(body, str):
            body = json.loads(body)

        notification, error = validate_notification(body)

        if error:
            return response(400, {"error": error})

        # Delivery will be added after local validation is tested.
        return response(200, {
            "status": "validated",
            "message": "Request validated. No notification was sent.",
            "notification": notification,
        })

    except (json.JSONDecodeError, AttributeError, TypeError):
        return response(400, {"error": "Invalid request body."})

