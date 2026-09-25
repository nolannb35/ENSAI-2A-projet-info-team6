import os

import requests


def research_api_by_title(movie_title):

    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": os.environ["API_KEY"],
        "query": movie_title,
        "language": "fr-FR"
    }

    data = requests.get(url, params=params).json()

    if data.get("results"):

        movie_id = data["results"][0]["id"]

        url = f"https://api.themoviedb.org/3/movie/{movie_id}"


        details = requests.get(url, params=params).json()

        plot = details["overview"]
        runtime = details["runtime"]
        title = details["title"]

        genres = [genre["name"] for genre in details["genres"]]
        information = dict()
        information["overview"] = plot
        information["runtime"] = runtime
        information["id"] = movie_id
        information["title"] = title
        information["genres"] = genres

        return information

    else:
        print("Aucun film trouvé")
        return None


result = research_api_by_title("Underground")

print(result)
