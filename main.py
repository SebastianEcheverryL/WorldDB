# Importaciones principales
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db import connect_db as get_connection
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/buscar", response_class=HTMLResponse)
def buscar(request: Request, pais: str = Form(...)):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT Name, Continent, Region, Population, LifeExpectancy
        FROM country
        WHERE Name LIKE %s
    """
    cursor.execute(query, ('%' + pais + '%',))
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return templates.TemplateResponse("result.html", {
        "request": request,
        "resultados": resultados,
        "pais": pais
    })
