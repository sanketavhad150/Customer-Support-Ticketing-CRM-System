from fastapi import APIRouter
from typing import Optional
from app.models import TicketIn, TicketUpdate
from app.controllers import ticket_controller

router = APIRouter(prefix="/api/tickets", tags=["Tickets"])

@router.post("")
def create(body: TicketIn):
    return ticket_controller.create_ticket(body)

@router.get("")
def list_all(status: Optional[str] = None, search: Optional[str] = None):
    return ticket_controller.list_tickets(status, search)

@router.get("/{ticket_id}")
def get(ticket_id: str):
    return ticket_controller.get_ticket(ticket_id)

@router.put("/{ticket_id}")
def update(ticket_id: str, body: TicketUpdate):
    return ticket_controller.update_ticket(ticket_id, body)
