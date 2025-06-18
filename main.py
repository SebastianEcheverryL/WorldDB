# Importaciones principales
from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db import connect_db as get_connection
from db import obtener_paises, obtener_ciudades
from fastapi.staticfiles import StaticFiles
import smtplib
from email.message import EmailMessage

app = FastAPI()
templates = Jinja2Templates(directory="Templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

EMAIL_ORIGEN = "secheverrylemos@gmail.com"
EMAIL_PASSWORD = "qimj gpva htuj xhzf"
EMAIL_DESTINO = "secheverrylemos@gmail.com"

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request,  "actual_page": "inicio"})

@app.get("/index", response_class=HTMLResponse)
def inicio(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "actual_page": "buscar"})

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
            "actual_page": "buscar",
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
            "actual_page": "buscar",
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
            "actual_page": "buscar_ciudad",
            "resultados": resultados,
            "ciudad": ciudad
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

@app.get("/paises", response_class=HTMLResponse)
async def listar_paises(request: Request):
    try:
        paises = obtener_paises()
        return templates.TemplateResponse("paises.html", {"request": request, "actual_page": "paises","paises": paises})
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

@app.get("/ciudades", response_class=HTMLResponse)
async def listar_ciudades(request: Request):
    try:
        ciudades = obtener_ciudades()
        return templates.TemplateResponse("ciudades.html", {"request": request, "actual_page": "ciudades","ciudades": ciudades})
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

@app.get("/contact", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request, "actual_page": "contact"})

@app.post("/contact")
async def enviar_contacto(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    mensaje: str = Form(...)
):
    # Crea el mensaje de correo
    msg = EmailMessage()
    msg["Subject"] = "Nuevo mensaje de contacto WorldDB"
    msg["From"] = EMAIL_ORIGEN
    msg["To"] = EMAIL_DESTINO
    msg.set_content(
        f"Nombre: {nombre}\nCorreo: {email}\n\nMensaje:\n{mensaje}"
    )

    # Envía el correo (ejemplo con Gmail)
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ORIGEN, EMAIL_PASSWORD)
            smtp.send_message(msg)
        mensaje_exito = "¡Mensaje enviado correctamente!"
    except Exception as e:
        mensaje_exito = f"Error al enviar el mensaje: {e}"
    return templates.TemplateResponse(
        "contact.html",
        {"request": request, "mensaje_exito": mensaje_exito}
    )

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))  # Usar el puerto que Render asigna
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

    # To run the application, use the command:
    # uvicorn main:app --reload
    # This will start the FastAPI application on http://localhost:8000
    # You can access the application in your web browser.