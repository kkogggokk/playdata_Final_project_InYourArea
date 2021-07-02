from fastapi import FastAPI, Request
from fastapi import responses
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles # Import staticFiles 
from .library.helpers import * # app/library/helpers.py 가져와서 app/pages에 있는 md파일 가져오기 

app = FastAPI()
templates = Jinja2Templates(directory="templates") # templage 설정해주기 
app.mount("/static", StaticFiles(directory="static"), name="static") # mount the static directory

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("home.md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})
    
@app.get("/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, page_name: str):
    data = openfile(page_name+".md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})
