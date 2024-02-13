from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact, User
from src.schemas.contacts import ContactSchema, ContactUpdateSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession, user: User):
    """
    The get_contacts function returns a list of contacts for the user.
        
    
    :param limit: int: Limit the number of contacts returned
    :param offset: int: Skip the first n records
    :param db: AsyncSession: Pass a database connection to the function
    :param user: User: Filter the contacts by user
    :return: A list of contacts
    :doc-author: Trelent
    """
    sq = select(Contact).filter_by(user=user).offset(offset).limit(limit)
    contacts = await db.execute(sq)
    return contacts.scalars().all()


async def get_all_contacts(limit: int, offset: int, db: AsyncSession):
    """
    The get_all_contacts function returns a list of all contacts in the database.
        
    
    :param limit: int: Limit the number of contacts returned
    :param offset: int: Skip the first n rows of data
    :param db: AsyncSession: Pass in the database session to the function
    :return: A list of contact objects
    :doc-author: Trelent
    """
    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession, user: User):
    """
    The get_contact function returns a contact object from the database.
    
    :param contact_id: int: Filter the query by contact id
    :param db: AsyncSession: Pass in the database session
    :param user: User: Filter the contacts by user
    :return: A contact object
    :doc-author: Trelent
    """
    sq = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(sq)
    return contact.scalar_one_or_none()


async def create_todo(body: ContactSchema, db: AsyncSession, user: User):
    """
    The create_todo function creates a new todo item.
    
    :param body: ContactSchema: Validate the request body
    :param db: AsyncSession: Pass the database connection to the function
    :param user: User: Get the user who is making the request
    :return: A contact object
    :doc-author: Trelent
    """
    contact = Contact(**body.model_dump(exclude_unset=True), user=user)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdateSchema, db: AsyncSession, user: User):
    """
    The update_contact function updates a contact in the database.
    
    :param contact_id: int: Identify the contact that we want to update
    :param body: ContactUpdateSchema: Validate the request body
    :param db: AsyncSession: Pass a database session to the function
    :param user: User: Get the user from the request
    :return: A contact
    :doc-author: Trelent
    """
    sq = select(Contact).filter_by(id=contact_id, user=user)
    result = await db.execute(sq)
    contact = result.scalar_one_or_none()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.data = body.data
        await db.commit()
        await db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: AsyncSession, user: User):
    """
    The remove_contact function removes a contact from the database.
    
    :param contact_id: int: Specify which contact to remove
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Identify the user who is making the request
    :return: A contact object if the contact was found and deleted, or none if it wasn't
    :doc-author: Trelent
    """
    sq = select(Contact).filter_by(id=contact_id, user=user)
    result = await db.execute(sq)
    contact = result.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact
