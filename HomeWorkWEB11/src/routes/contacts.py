from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas import ContactResponse, ContactSchema, ContactUpdateSchema
from src.repository import contacts as repository_contacts


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(
    limit: int = Query(10, ge=10, le=500),
    offset: int = Query(0, ge=0, le=200),
    db: AsyncSession = Depends(get_db),
):
    contact = await repository_contacts.get_contacts(limit, offset, db)
    return contact


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND!",
        )
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.create_contact(body, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    body: ContactUpdateSchema,
    contact_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND!",
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact(
    contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)
):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND!",
        )
    return contact
