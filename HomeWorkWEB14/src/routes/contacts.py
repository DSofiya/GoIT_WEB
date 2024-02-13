from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User, Role
from src.services.roles import RoleAccess
from src.services.auth import auth_service
from src.database.db import get_db
from src.schemas.contacts import ContactResponse, ContactSchema, ContactUpdateSchema
from src.repository import contacts as repository_contacts


router = APIRouter(prefix="/contacts", tags=["contacts"])
access_to_route_all = RoleAccess([Role.admin, Role.moderator])

@router.get("/", response_model=List[ContactResponse])
async def get_contacts(
    limit: int = Query(10, ge=10, le=500),
    offset: int = Query(0, ge=0, le=200),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    """
    The get_contacts function returns a list of contacts for the current user.
    The limit and offset parameters are used to paginate the results.

    :param limit: int: Limit the number of contacts returned.
    :param ge: Specify the minimum value of a parameter.
    :param le: Limit the number of contacts returned.
    :param offset: int: Get the next set of data from the database.
    :param ge: Specify the minimum value that can be passed in.
    :param le: Limit the number of contacts that can be returned.
    :param db: AsyncSession: Pass the database connection to the function.
    :param user: User: Get the user from the database.
    :return: A list of contacts.
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contacts(limit, offset, db, user)
    return contact


@router.get("/all", response_model=list[ContactResponse], dependencies=[Depends(access_to_route_all)])
async def get_all_todos(
    limit: int = Query(10, ge=10, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    """
    The get_all_todos function returns a list of all todos in the database.

    :param limit: int: Limit the number of contacts returned.
    :param ge: Specify a minimum value for the limit parameter.
    :param le: Limit the number of results returned.
    :param offset: int: Specify the number of records to skip before returning results.
    :param ge: Specify a minimum value.
    :param db: AsyncSession: Access the database.
    :param user: User: Get the current user from the auth_service.
    :return: A list of contacts.
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_all_contacts(limit, offset, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1),db: AsyncSession = Depends(get_db),user: User = Depends(auth_service.get_current_user),):
    """
    The get_contact function returns a contact by its id.
    
    :param contact_id: int: Get the contact id from the url
    :param db: AsyncSession: Pass the database session to the repository
    :param user: User: Get the current user from the database
    :param : Get the contact id from the url
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND!",
        )
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    body: ContactSchema,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    """
    The create_contact function creates a new contact in the database.
    The function takes in a ContactSchema object, which is validated by pydantic.
    If the validation fails, an error will be thrown and caught by FastAPI's exception handler.
    If it passes validation, then we create a new contact using our repository_contacts module.

    :param body: ContactSchema: Validate the request body.
    :param db: AsyncSession: Pass the database session to the repository layer.
    :param user: User: Get the user that is currently logged in.
    :return: A ContactResponse object.
    :doc-author: Trelent
    """
    contact = await repository_contacts.create_contact(body, db, user)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactUpdateSchema,contact_id: int = Path(ge=1),db: AsyncSession = Depends(get_db),user: User = Depends(auth_service.get_current_user),):
    contact = await repository_contacts.update_contact(contact_id, body, db, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND!",
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact(
    contact_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    """
    The delete_contact function deletes a contact from the database.
    The function takes in an integer representing the id of the contact to be deleted,
    and returns a dictionary containing information about that contact.

    :param contact_id: int: Get the contact id from the URL path.
    :param db: AsyncSession: Pass the database session to the repository layer.
    :param user: User: Get the current user from the auth_service.
    :return: A ContactResponse object.
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND!",
        )
    return contact
