from pydantic import BaseModel
from typing import Optional

class TicketIn(BaseModel):
    customer_name: str
    customer_email: str
    subject: str
    description: str

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    note: Optional[str] = None
