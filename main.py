# Importaciones principales
from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db import connect_db as get_connection
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})

@app.get("/index", response_class=HTMLResponse)
def inicio(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/buscar", response_class=HTMLResponse)
def buscar_get(request: Request, pais: str = Query(...)):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT Name, Continent, Region, Population, LifeExpectancy
            FROM country
            WHERE Name LIKE %s
        """
        cursor.execute(query, ('%' + pais + '%',))
        resultados = cursor.fetchall()

        # Calcula promedios globales ANTES de cerrar el cursor
        cursor.execute("SELECT AVG(Population) as avg_pop, AVG(LifeExpectancy) as avg_life FROM country")
        promedios = cursor.fetchone()

        cursor.close()
        conn.close()

        return templates.TemplateResponse("result.html", {
            "request": request,
            "resultados": resultados,
            "pais": pais,
            "avg_pop": int(promedios["avg_pop"]) if promedios["avg_pop"] else 0,
            "avg_life": float(promedios["avg_life"]) if promedios["avg_life"] else 0,
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

@app.post("/buscar", response_class=HTMLResponse)
def buscar(request: Request, pais: str = Form(...)):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT Name, Continent, Region, Population, LifeExpectancy
            FROM country
            WHERE Name LIKE %s
        """
        cursor.execute(query, ('%' + pais + '%',))
        resultados = cursor.fetchall()

        # Calcula promedios globales ANTES de cerrar el cursor
        cursor.execute("SELECT AVG(Population) as avg_pop, AVG(LifeExpectancy) as avg_life FROM country")
        promedios = cursor.fetchone()

        cursor.close()
        conn.close()

        return templates.TemplateResponse("result.html", {
            "request": request,
            "resultados": resultados,
            "pais": pais,
            "avg_pop": int(promedios["avg_pop"]) if promedios["avg_pop"] else 0,
            "avg_life": float(promedios["avg_life"]) if promedios["avg_life"] else 0,
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

@app.post("/buscar_ciudad", response_class=HTMLResponse)
def buscar_ciudad(request: Request, ciudad: str = Form(...)):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT Name, CountryCode, District, Population
            FROM city
            WHERE Name LIKE %s
        """
        cursor.execute(query, ('%' + ciudad + '%',))
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return templates.TemplateResponse("result_ciudad.html", {
            "request": request,
            "resultados": resultados,
            "ciudad": ciudad
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})


