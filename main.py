import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 \
                (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 \
                (KHTML, like Gecko) \
                Chrome/123.0.0.0 Safari/537.36'
}


def get_response(url: str) -> requests.models.Response:
    return requests.get(url, headers=HEADERS)


def get_best_buy_price(item: str) -> dict:
    url = ''
    response = get_response(url)
    # check if response is valid
    if response.status_code == 200:
        return {}
    else:
        return {'error': 'Invalid response'}


def get_walmart_price(item: str) -> dict:
    url = ''
    response = get_response(url)
    # check if response is valid
    if response.status_code == 200:
        return {}
    else:
        return {'error': 'Invalid response'}


def get_newegg_price(item: str) -> dict:
    url = ''
    response = get_response(url)
    # check if response is valid
    if response.status_code == 200:
        return {}
    else:
        return {'error': 'Invalid response'}


# Main
if __name__ == "__main__":
    pass
