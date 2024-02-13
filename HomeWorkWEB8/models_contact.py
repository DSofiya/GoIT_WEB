from mongoengine import connect, Document, StringField, BooleanField

connect(
    db="hw08",
    host="mongodb+srv://dsonya:70Venipa@cluster0.oiopl60.mongodb.net/?retryWrites=true&w=majority",
)


class Contact(Document):
    full_name = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    message_sent = BooleanField(default=False)
    phone= StringField()
    preferred_contact_method = StringField(choices=["email", "sms"], default="email")
