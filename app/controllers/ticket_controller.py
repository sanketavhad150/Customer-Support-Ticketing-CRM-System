import datetime
from fastapi import HTTPException
from app.database import get_db
from app.models import TicketIn, TicketUpdate

def create_ticket(body: TicketIn):
    conn = get_db()
    row = conn.execute("SELECT COUNT(*) as c FROM tickets").fetchone()
    ticket_id = f"TKT-{row['c'] + 1:03d}"
    now = datetime.datetime.utcnow().isoformat()
    conn.execute(
        "INSERT INTO tickets (ticket_id,customer_name,customer_email,subject,description,status,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?)",
        (ticket_id, body.customer_name, body.customer_email, body.subject, body.description, "Open", now, now)
    )
    conn.commit()
    conn.close()
    return {"ticket_id": ticket_id, "created_at": now}

def list_tickets(status=None, search=None):
    conn = get_db()
    query = "SELECT ticket_id,customer_name,customer_email,subject,status,created_at FROM tickets WHERE 1=1"
    params = []
    if status:
        query += " AND status=?"
        params.append(status)
    if search:
        query += " AND (customer_name LIKE ? OR customer_email LIKE ? OR ticket_id LIKE ? OR description LIKE ? OR subject LIKE ?)"
        s = f"%{search}%"
        params.extend([s, s, s, s, s])
    query += " ORDER BY id DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_ticket(ticket_id: str):
    conn = get_db()
    row = conn.execute("SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,)).fetchone()
    if not row:
        raise HTTPException(404, "Ticket not found")
    notes = conn.execute(
        "SELECT note_text,created_at FROM notes WHERE ticket_id=? ORDER BY id", (ticket_id,)
    ).fetchall()
    conn.close()
    data = dict(row)
    data["notes"] = [dict(n) for n in notes]
    return data

def update_ticket(ticket_id: str, body: TicketUpdate):
    conn = get_db()
    row = conn.execute("SELECT id FROM tickets WHERE ticket_id=?", (ticket_id,)).fetchone()
    if not row:
        raise HTTPException(404, "Ticket not found")
    now = datetime.datetime.utcnow().isoformat()
    if body.status:
        conn.execute("UPDATE tickets SET status=?, updated_at=? WHERE ticket_id=?", (body.status, now, ticket_id))
    if body.note:
        conn.execute("INSERT INTO notes (ticket_id,note_text,created_at) VALUES (?,?,?)", (ticket_id, body.note, now))
    conn.commit()
    conn.close()
    return {"success": True, "updated_at": now}
