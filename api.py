from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router
from fastapi.responses import RedirectResponse
import os

app = FastAPI()

# 🔥 Configurar CORS (Si usas frontend separado)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📌 Servir `public/` en `/public/` (NO en `/` para evitar que bloquee rutas)
app.mount("/public", StaticFiles(directory="public", html=True), name="public")

# 📌 Redirigir `/` a `home.html` manualmente
@app.get("/")
async def serve_home():
    return RedirectResponse(url="/public/home.html")

# 📌 Servir `favicon.ico` sin bloquear rutas
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    favicon_path = os.path.join(os.getcwd(), "public", "favicon.ico")
    if not os.path.exists(favicon_path):
        return {"error": "Archivo favicon.ico no encontrado"}
    return FileResponse(favicon_path)

@app.get("/dashboard")
async def serve_dashboard():
    return RedirectResponse(url="/public/dashboard.html")


# 📌 Incluir rutas de autenticación
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=3100, reload=True)
