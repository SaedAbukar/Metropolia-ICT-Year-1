import requests


def fetch_chuck_norris_joke():
    url = "https://api.chucknorris.io/jokes/random"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_response = response.json()
            return json_response["value"]
        else:
            return "Error occurred while fetching the joke."
    except requests.exceptions.RequestException as e:
        return f'The request could not be performed: {e}'


print(fetch_chuck_norris_joke())
