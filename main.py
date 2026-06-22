import os
import shlex
import subprocess
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    destination: str = "dir:/tmp/artifact_output"
    max_size_mb: int = 100
    skopeo_args: str = "--dest-tls-verify=false"

    @property
    def max_size(self) -> int:
        return self.max_size_mb * 1024 * 1024


settings = Settings()
STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/docs", include_in_schema=False)
def docs() -> HTMLResponse:
    """Geeft de Swagger UI-documentatiepagina terug met lokale statische bestanden."""
    return get_swagger_ui_html(
        openapi_url=app.openapi_url or "/openapi.json",
        title="Skopeo Upload - Swagger UI",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        oauth2_redirect_url=None,
    )

INDEX_HTML = (STATIC_DIR / "index.html").read_text().format(destination=settings.destination)

@app.get("/", response_class=HTMLResponse)
def index():
    """Geeft de startpagina terug met het uploadformulier."""
    return INDEX_HTML

@app.post("/upload", response_class=HTMLResponse)
async def upload(file: UploadFile = File(...)):
    """
    Ontvangt een OCI-archive (.tar), slaat het tijdelijk op en kopieert het
    naar de geconfigureerde bestemming via skopeo. Toont het resultaat als HTML.
    """
    if file.size and file.size > settings.max_size:
        raise HTTPException(status_code=413, detail=f"File too large (max {settings.max_size_mb} MB).")

    contents = await file.read()
    if len(contents) > settings.max_size:
        raise HTTPException(status_code=413, detail=f"File too large (max {settings.max_size_mb} MB).")

    if not file.filename or not file.filename.endswith(".tar"):
        raise HTTPException(status_code=400, detail="Only .tar files are accepted.")

    with tempfile.NamedTemporaryFile(suffix=".tar", delete=False) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            ["skopeo", "copy", *shlex.split(settings.skopeo_args), f"oci-archive:{tmp_path}", settings.destination],
            capture_output=True, text=True
        )
        output = result.stdout + result.stderr
        status = "Uitgevoerd" if result.returncode == 0 else "Gefaald!"
        return f"<pre>{status}\n\n{output}</pre><a href='/'>Terug</a>"
    finally:
        os.unlink(tmp_path)
