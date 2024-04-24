import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}


def get_response(url: str) -> requests.models.Response:
    return requests.get(url, headers=HEADERS)


def get_best_buy_price(item: str) -> dict:
    str_item = quote_plus(item)
    url = f'https://www.bestbuy.com/site/searchpage.jsp?st={str_item}&intl=nosplash'  # nopep8
    response = get_response(url)
    # Check if response is valid
    if response.status_code == 200:
        # Get items
        best_buy_search_page_soup = BeautifulSoup(
            response.content, "html.parser")
        items = best_buy_search_page_soup.find_all('li', class_='sku-item')

        # Check if there are items
        if not items:
            raise Exception("No items found in Best Buy search page")

        # If we reach here - there is at least one item
        item = items[0]

        # Get item name
        item_name = item.find('h4', class_='sku-title').text

        # Get item page link: inside the h4 tag there is a <a> tag with the link
        item_page_link = item.find('h4', class_='sku-title').a['href']
        full_item_page_link = f'https://www.bestbuy.com{item_page_link}&intl=nosplash'  # nopep8

        # Get item page response
        item_page_response = get_response(full_item_page_link)
        # Check if response is valid
        if item_page_response.status_code == 200:
            # Get item price: class "priceView-hero-price priceView-customer-price"
            item_page_soup = BeautifulSoup(item_page_response.content, "html.parser")  # nopep8
            item_price = item_page_soup.find('div', class_='priceView-hero-price priceView-customer-price').span.text  # nopep8
            if not item_price:
                raise Exception("Item price not found in item page")

            # If we reach here - we have the item price
            # extract the price as a number from the string
            item_price = float(item_price.replace('$', '').replace(',', '').strip())  # nopep8
            return {"Site": "Best Buy", "Item title name": item_name, "Price(USD)": item_price, "Link": full_item_page_link}  # nopep8
        else:
            raise Exception("Invalid item page response")
    else:
        raise Exception("Invalid Best Buy search page response")


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
    print(get_best_buy_price('iPhone'))
