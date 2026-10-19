
import json
import unittest

from handler import lambda_handler


class NotificationHandlerTests(unittest.TestCase):

    def test_valid_email_request(self):
        event = {
            "body": json.dumps({
                "recipientName": "Alex",
                "channel": "email",
                "destination": "alex@example.com",
                "message": "Hello from CloudNotify",
            })
        }

        result = lambda_handler(event, None)

        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(
            json.loads(result["body"])["status"],
            "validated",
        )

    def test_invalid_channel(self):
        event = {
            "body": json.dumps({
                "recipientName": "Alex",
                "channel": "fax",
                "destination": "alex@example.com",
                "message": "Hello",
            })
        }

        result = lambda_handler(event, None)

        self.assertEqual(result["statusCode"], 400)

    def test_invalid_email(self):
        event = {
            "body": json.dumps({
                "recipientName": "Alex",
                "channel": "email",
                "destination": "not-an-email",
                "message": "Hello",
            })
        }

        result = lambda_handler(event, None)

        self.assertEqual(result["statusCode"], 400)


if __name__ == "__main__":
    unittest.main()

