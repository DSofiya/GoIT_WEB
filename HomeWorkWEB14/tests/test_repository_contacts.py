import unittest
from unittest.mock import AsyncMock, patch, MagicMock, Mock
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.contacts import ContactSchema
from src.database.models import Contact, User
from src.repository.contacts import (
    get_all_contacts,
    get_contacts,
    get_contact,
    create_todo,
    remove_contact,
    update_contact,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.session = AsyncMock(spec=AsyncSession)
        self.contact = Contact(id=1, first_name='test',last_name ='testovich', email='test email', phone_number='09600000022', birthday='12.03.2000')
        self.contacts = [self.contact,
                        Contact(id=2, first_name=self.contact.first_name, last_name=self.contact.last_name, 
                                email='test_email', phone_number='test_phone', birthday=self.contact.birthday),
                        Contact(id=3, first_name=self.contact.first_name, last_name=self.contact.last_name,
                                 email='test_email', phone_number='test_phone', birthday=self.contact.birthday)
                        ]

    
    async def test_get_contacts(self):
        limit = 10
        offset = 0
        contacts= self.contacts
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts(limit, offset, self.session, User())
        self.assertEqual(result, contacts)

    
    async def test_get_all_contacts(self):
        contact = Contact()
        limit = 10
        offset = 0
        contact = self.contacts
        mocked_contact = MagicMock()
        mocked_contact.scalars.return_value.all.return_value = contact
        self.session.execute.return_value = mocked_contact
        result = await get_all_contacts(limit, offset, self.session)
        self.assertEqual(result, contact)

    
    async def test_get_contact_not_found(self):
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = None
        self.session.execute.return_value = mocked_contact
        result = await get_contact(0, self.session, User())
        self.assertIsNone(result)

    
    async def test_create_contact(self):
        body = ContactSchema(
            first_name=self.contact.first_name,
            last_name='Test S',
            email='Test email',
            phone_number='09600002222',
            birthday='12.03.2000',  
        )
        result = await create_todo(body, self.session, User())
        self.assertEqual(result.first_name, self.contact.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertTrue(hasattr(result, "id"))

    
    async def test_update_contact_found(self):
        body = ContactSchema(
            first_name=self.contact.first_name,
            last_name=self.contact.last_name,
            email=self.contact.email,
            phone_number=self.contact.phone_number,
            birthday='12.05.2000',
        )
       
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = self.contact
        self.session.execute.return_value = mocked_contact
        result = await update_contact(contact_id=1, body=body, db=self.session, user=User())
        self.assertEqual(result, self.contact)
        
    
    async def test_update_contact_not_found(self):
        body = ContactSchema(
            first_name=self.contact.first_name,
            last_name=self.contact.last_name,
            email=self.contact.email,
            phone_number=self.contact.phone_number,
            birthday='12.05.2000',
        )
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = None
        self.session.execute.return_value = mocked_contact
        result = await update_contact(contact_id=1, body=body, db=self.session, user=User())
        self.assertIsNone(result)

    
    async def test_remove_contact(self):
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = self.contact
        self.session.execute.return_value = mocked_contact
        result = await remove_contact(contact_id=1, db=self.session, user=User())
        self.assertEqual(result, self.contact)

    
    async def test_remove_contact_not_found(self):
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = None
        self.session.execute.return_value = mocked_contact
        result = await remove_contact(contact_id=1, db=self.session, user=User())
        self.assertIsNone(result, 'db returned object')

    
if __name__ == "__main__":
    unittest.main()