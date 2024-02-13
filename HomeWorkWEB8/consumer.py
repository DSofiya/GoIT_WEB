import json
import pika
from models_contact import Contact


credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()


def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

    message = json.loads(body)
    contact_id = message["contact_id"]
    contact = Contact.objects.get(id=contact_id)

    print(f"Sending email to {contact.email} for contact {contact.id}")
    contact.message_sent = True
    contact.save()

    print(f"Email sent to {contact.email} for contact {contact.id}")


channel.basic_consume(
    queue="email_hello_world", on_message_callback=callback, auto_ack=True
)

print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
