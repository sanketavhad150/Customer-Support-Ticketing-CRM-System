from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Pages"])
templates = Jinja2Templates(directory="templates")

# @router.get("/")
# def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})
@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

# @router.get("/create")
# def create_page(request: Request):
#     return templates.TemplateResponse("create.html", {"request": request})
@router.get("/create")
def create_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="create.html",
        context={}
    )

@router.get("/ticket/{ticket_id}")
def ticket_page(request: Request, ticket_id: str):
    return templates.TemplateResponse(
        request=request,
        name="ticket.html",
        context={"ticket_id": ticket_id}
    )