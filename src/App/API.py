import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.Control.MovieControl import movie_router
from src.Control.UserControl import user_router
from src.utils.log_utils import initialize_logs


def run_app():
    initialize_logs("Ensai Cinema Club")
    app = FastAPI(title="Projet Info 2A", description="Example project for ENSAI students")

    app.include_router(user_router)

    app.include_router(movie_router)

    @app.get("/", include_in_schema=False)
    async def redirect_to_docs():
        """Redirect to the API documentation"""
        return RedirectResponse(url="/docs")

    uvicorn.run(app, port=8000, host="0.0.0.0")
