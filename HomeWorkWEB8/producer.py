import json
import random
from faker import Faker
from models_contact import Contact
import pika

fake = Faker()

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()
channel.queue_declare(queue="email_hello_world")
    

for _ in range(5):  
    full_name = fake.name()
    email = fake.email()
    phone = fake.phone_number()
    preferred_contact_method = random.choice(["email", "sms"])

    contact = Contact(
        full_name=full_name,
        email=email,
        phone=phone,
        preferred_contact_method=preferred_contact_method,
    )
    contact.save()
    
    message = {"contact_id": str(contact.id)}
    channel.basic_publish(
            exchange="", routing_key="email_hello_world", body=json.dumps(message)
        )
    print(f"Sent contact {contact.id} to the email queue")
   
connection.close()
