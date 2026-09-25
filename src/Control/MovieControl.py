from fastapi import APIRouter, Depends, HTTPException, status

from src.Service.MovieService import MovieService

movie_router = APIRouter(prefix="/movies", tags=["Movies"])

def get_player_service():
    """Dependency provider."""
    return MovieService()

@movie_router.get("/{tmdb_id}", status_code=status.HTTP_200_OK)
def get_movie_by_id(tmdb_id: int):
    movie_service = Depends(get_player_service)
    try:
        my_movie = movie_service.get_by_id(tmdb_id)
        return my_movie
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Movie with id [{}] not found".format(tmdb_id),
        ) from FileNotFoundError
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid request") from Exception
